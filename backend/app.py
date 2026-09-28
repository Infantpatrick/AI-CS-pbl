import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
import uuid
import hashlib
import secrets
from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.schemas import PredictionRequest, RiskResponse, HealthResponse, ModelInfoResponse, UserCreate, UserLogin, UserResponse
from src.model.risk_assessment import assess_email_risk

app = FastAPI(
    title="PhishGuard AI",
    description="API for the AI-Based Email Phishing Detection using BERT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:3000", "http://localhost:8000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite Auth System
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'phishguard.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            email TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS oauth_connections (
            user_id TEXT NOT NULL,
            provider TEXT NOT NULL,
            provider_user_id TEXT NOT NULL,
            PRIMARY KEY (user_id, provider)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS gmail_tokens (
            user_id TEXT PRIMARY KEY,
            access_token TEXT NOT NULL,
            refresh_token TEXT,
            expires_at REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            message_id TEXT NOT NULL,
            subject TEXT,
            sender TEXT,
            prediction TEXT,
            phishing_probability REAL,
            legitimate_probability REAL,
            confidence REAL,
            risk_level TEXT,
            urls_found INTEGER,
            url_indicators TEXT,
            risk_reasons TEXT,
            body TEXT,
            analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT email FROM sessions WHERE session_id = ?", (session_id,))
        session = c.fetchone()
        if not session:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        email = session["email"]
        c.execute("SELECT id, name, email FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return dict(user)

@app.post("/auth/register")
def register(user: UserCreate):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT email FROM users WHERE email = ?", (user.email,))
        if c.fetchone():
            raise HTTPException(status_code=409, detail="An account with this email already exists.")
        
        user_id = str(uuid.uuid4())
        c.execute(
            "INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?)",
            (user_id, user.name, user.email, hash_password(user.password))
        )
        conn.commit()
    return {"message": "Account created successfully. Please sign in."}

@app.post("/auth/login", response_model=UserResponse)
def login(user: UserLogin, response: Response):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (user.email,))
        db_user = c.fetchone()
        
        if not db_user or db_user["password_hash"] != hash_password(user.password):
            raise HTTPException(status_code=401, detail="Email or password is incorrect.")
        
        session_id = str(uuid.uuid4())
        c.execute("INSERT INTO sessions (session_id, email) VALUES (?, ?)", (session_id, user.email))
        conn.commit()
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=3600 * 24
    )
    
    return UserResponse(id=db_user["id"], name=db_user["name"], email=db_user["email"])

@app.post("/auth/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            conn.commit()
    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}

@app.get("/auth/me", response_model=UserResponse)
def get_me(user: dict = Depends(get_current_user)):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM gmail_tokens WHERE user_id = ?", (user["id"],))
        has_gmail = c.fetchone() is not None
    user["has_gmail"] = has_gmail
    return UserResponse(**user)


# ==========================================
# OAUTH ENDPOINTS (GOOGLE & GITHUB)
# ==========================================
import urllib.parse
import httpx
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"

GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
GITHUB_REDIRECT_URI = "http://localhost:8000/auth/github/callback"

@app.get("/auth/google/url")
def google_auth_url(response: Response):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    
    state = secrets.token_urlsafe(32)
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    redirect = RedirectResponse(url)
    redirect.set_cookie(key="oauth_state", value=state, httponly=True, samesite="lax", secure=False, max_age=300)
    return redirect

@app.get("/auth/google/callback")
async def google_auth_callback(request: Request, response: Response, code: str = None, state: str = None, error: str = None):
    if error:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    if not state:
        raise HTTPException(status_code=400, detail="Missing state parameter")
        
    # Check if this is a Gmail connection callback
    if state.startswith("gmail_connect:"):
        user_id = state.split("gmail_connect:")[1]
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(token_url, data=token_data)
            if res.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to exchange authorization code for Gmail tokens")
            tokens = res.json()
            
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="Missing access token in Google response")
            
        with get_db() as conn:
            c = conn.cursor()
            c.execute("SELECT 1 FROM gmail_tokens WHERE user_id = ?", (user_id,))
            exists = c.fetchone()
            if exists:
                if refresh_token:
                    c.execute("UPDATE gmail_tokens SET access_token = ?, refresh_token = ? WHERE user_id = ?", (access_token, refresh_token, user_id))
                else:
                    c.execute("UPDATE gmail_tokens SET access_token = ? WHERE user_id = ?", (access_token, user_id))
            else:
                c.execute("INSERT INTO gmail_tokens (user_id, access_token, refresh_token) VALUES (?, ?, ?)", (user_id, access_token, refresh_token))
            conn.commit()
            
        return RedirectResponse("http://localhost:5173/inbox")
        
    # Otherwise, this is a Google Login callback
    saved_state = request.cookies.get("oauth_state")
    if not saved_state or saved_state != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
        
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.post(token_url, data=token_data)
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")
        tokens = res.json()
        
    id_token_str = tokens.get("id_token")
    if not id_token_str:
        raise HTTPException(status_code=400, detail="Missing ID token in Google response")
        
    try:
        id_info = id_token.verify_oauth2_token(
            id_token_str, google_requests.Request(), GOOGLE_CLIENT_ID
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID token")
        
    email = id_info.get("email")
    name = id_info.get("name", "Unknown")
    provider_user_id = id_info.get("sub")
    
    if not email or not provider_user_id:
        raise HTTPException(status_code=400, detail="Incomplete Google profile information")
        
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        
        if user:
            user_id = user["id"]
        else:
            user_id = str(uuid.uuid4())
            c.execute(
                "INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?)",
                (user_id, name, email, "oauth_google")
            )
            
        c.execute("SELECT 1 FROM oauth_connections WHERE user_id = ? AND provider = 'google'", (user_id,))
        if not c.fetchone():
            c.execute(
                "INSERT INTO oauth_connections (user_id, provider, provider_user_id) VALUES (?, ?, ?)",
                (user_id, "google", provider_user_id)
            )
            
        session_id = str(uuid.uuid4())
        c.execute("INSERT INTO sessions (session_id, email) VALUES (?, ?)", (session_id, email))
        conn.commit()
        
    redirect = RedirectResponse("http://localhost:5173/dashboard")
    redirect.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=3600 * 24
    )
    redirect.delete_cookie("oauth_state")
    return redirect

@app.get("/auth/github/url")
def github_auth_url():
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GitHub OAuth not configured")
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "user:email"
    }
    url = "https://github.com/login/oauth/authorize?" + urllib.parse.urlencode(params)
    return RedirectResponse(url)

@app.get("/auth/github/callback")
def github_auth_callback(code: str, response: Response):
    # This would securely exchange the code for tokens and login/create the user
    # For now, redirect back to frontend dashboard
    return RedirectResponse("http://localhost:5173/dashboard")

@app.get("/auth/gmail/url")
def gmail_auth_url(user: dict = Depends(get_current_user)):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/gmail.readonly",
        "access_type": "offline",
        "prompt": "consent",
        "state": f"gmail_connect:{user['id']}"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return RedirectResponse(url)

@app.get("/auth/gmail/callback")
async def gmail_auth_callback(code: str, state: str, error: str = None):
    if error:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {error}")
    
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://localhost:8000/auth/gmail/callback",
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.post(token_url, data=token_data)
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code for Gmail tokens")
        tokens = res.json()
        
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    
    if not access_token:
        raise HTTPException(status_code=400, detail="Missing access token in Google response")
        
    # state contains the user_id
    user_id = state
    
    with get_db() as conn:
        c = conn.cursor()
        # Insert or replace
        c.execute("SELECT 1 FROM gmail_tokens WHERE user_id = ?", (user_id,))
        exists = c.fetchone()
        if exists:
            if refresh_token:
                c.execute("UPDATE gmail_tokens SET access_token = ?, refresh_token = ? WHERE user_id = ?", (access_token, refresh_token, user_id))
            else:
                c.execute("UPDATE gmail_tokens SET access_token = ? WHERE user_id = ?", (access_token, user_id))
        else:
            c.execute("INSERT INTO gmail_tokens (user_id, access_token, refresh_token) VALUES (?, ?, ?)", (user_id, access_token, refresh_token))
        conn.commit()
        
    return RedirectResponse("http://localhost:5173/dashboard")

# ==========================================
# GMAIL & ANALYSIS ENDPOINTS
# ==========================================
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import traceback

from google.auth.exceptions import RefreshError

def get_gmail_service(user_id: str):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT access_token, refresh_token FROM gmail_tokens WHERE user_id = ?", (user_id,))
        token_data = c.fetchone()
        if not token_data:
            raise HTTPException(status_code=403, detail="Gmail not connected")
        
        creds = Credentials(
            token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET
        )
        
        return build('gmail', 'v1', credentials=creds), creds, token_data["access_token"]

@app.get("/api/gmail/inbox")
def get_inbox(user: dict = Depends(get_current_user)):
    try:
        service, creds, old_token = get_gmail_service(user["id"])
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=20).execute()
        
        if creds.token != old_token:
            with get_db() as conn:
                conn.cursor().execute("UPDATE gmail_tokens SET access_token = ? WHERE user_id = ?", (creds.token, user["id"]))
                conn.commit()
                
        messages = results.get('messages', [])
        
        inbox_data = []
        with get_db() as conn:
            c = conn.cursor()
            for msg in messages:
                msg_id = msg['id']
                message = service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
                payload = message.get('payload') or {}
                headers = payload.get('headers') or []
                
                subject = next((h.get('value', '(No subject)') for h in headers if h.get('name', '').lower() == 'subject'), '(No subject)')
                sender = next((h.get('value', 'Unknown sender') for h in headers if h.get('name', '').lower() == 'from'), 'Unknown sender')
                date = next((h.get('value', '') for h in headers if h.get('name', '').lower() == 'date'), '')
                
                c.execute("SELECT prediction, risk_level FROM analysis_results WHERE message_id = ?", (msg_id,))
                analysis = c.fetchone()
                
                if analysis:
                    risk_level = analysis["risk_level"]
                else:
                    risk_level = None
                
                inbox_data.append({
                    "id": msg_id,
                    "sender": sender,
                    "subject": subject,
                    "snippet": message.get('snippet', ''),
                    "date": date,
                    "risk_level": risk_level
                })
        return {"messages": inbox_data}
    except HttpError as e:
        raise HTTPException(status_code=502 if e.resp.status >= 500 else e.resp.status, detail=f"Gmail API error: {e.reason}")
    except RefreshError:
        raise HTTPException(status_code=401, detail="Gmail authentication failed or expired. Please reconnect.")
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

def extract_body(payload):
    if not payload:
        return ""
    mime_type = payload.get("mimeType")
    if mime_type in ["text/plain", "text/html"] and "data" in payload.get("body", {}):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", "ignore")
    
    body = ""
    for part in payload.get("parts", []):
        if part.get("mimeType") in ["text/plain", "text/html"]:
            if "data" in part.get("body", {}):
                body += base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", "ignore")
        elif "parts" in part:
            body += extract_body(part)
    return body

def extract_attachments(payload):
    attachments = []
    if not payload:
        return attachments
    for part in payload.get("parts", []):
        if part.get("filename") and part.get("body", {}).get("attachmentId"):
            attachments.append({
                "filename": part["filename"],
                "mimeType": part.get("mimeType", ""),
                "attachmentId": part["body"]["attachmentId"]
            })
        elif "parts" in part:
            attachments.extend(extract_attachments(part))
    return attachments

@app.get("/api/gmail/message/{message_id}")
def get_message(message_id: str, user: dict = Depends(get_current_user)):
    try:
        service, creds, old_token = get_gmail_service(user["id"])
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        
        if creds.token != old_token:
            with get_db() as conn:
                conn.cursor().execute("UPDATE gmail_tokens SET access_token = ? WHERE user_id = ?", (creds.token, user["id"]))
                conn.commit()
                
        payload = message.get('payload') or {}
        headers = payload.get('headers') or []
        
        subject = next((h.get('value', '(No subject)') for h in headers if h.get('name', '').lower() == 'subject'), '(No subject)')
        sender = next((h.get('value', 'Unknown sender') for h in headers if h.get('name', '').lower() == 'from'), 'Unknown sender')
        recipient = next((h.get('value', 'Unknown') for h in headers if h.get('name', '').lower() == 'to'), 'Unknown')
        date = next((h.get('value', '') for h in headers if h.get('name', '').lower() == 'date'), '')
        
        body = extract_body(payload)
        if not body:
            body = message.get('snippet', '')
            
        attachments = extract_attachments(payload)
        
        analysis = None
        with get_db() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM analysis_results WHERE message_id = ? AND user_id = ?", (message_id, user["id"]))
            row = c.fetchone()
            if row:
                analysis = dict(row)
        
        return {
            "id": message_id,
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "date": date,
            "body": body,
            "attachments": attachments,
            "extracted_urls": [],
            "analysis": analysis
        }
    except HttpError as e:
        raise HTTPException(status_code=502 if e.resp.status >= 500 else e.resp.status, detail=f"Gmail API error: {e.reason}")
    except RefreshError:
        raise HTTPException(status_code=401, detail="Gmail authentication failed or expired. Please reconnect.")
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

from pydantic import BaseModel

class AnalysisSaveRequest(BaseModel):
    message_id: str
    subject: str
    sender: str
    prediction: str
    phishing_probability: float
    legitimate_probability: float
    confidence: float
    risk_level: str
    urls_found: int
    url_indicators: list = []
    risk_reasons: list = []
    body: str = ""

@app.post("/api/analysis")
def save_analysis(req: AnalysisSaveRequest, user: dict = Depends(get_current_user)):
    result_id = str(uuid.uuid4())
    with get_db() as conn:
        c = conn.cursor()
        import json
        c.execute("""
            INSERT OR REPLACE INTO analysis_results (id, user_id, message_id, subject, sender, prediction, phishing_probability, legitimate_probability, confidence, risk_level, urls_found, url_indicators, risk_reasons, body)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (result_id, user["id"], req.message_id, req.subject, req.sender, req.prediction, req.phishing_probability, req.legitimate_probability, req.confidence, req.risk_level, req.urls_found, json.dumps(req.url_indicators), json.dumps(req.risk_reasons), req.body))
        conn.commit()
    return {"message": "Analysis saved successfully", "id": result_id}

@app.get("/api/analysis/stats")
def get_dashboard_stats(user: dict = Depends(get_current_user)):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM analysis_results WHERE user_id = ?", (user["id"],))
        total = c.fetchone()["total"]
        c.execute("SELECT COUNT(*) as phishing FROM analysis_results WHERE user_id = ? AND risk_level = 'HIGH'", (user["id"],))
        phishing = c.fetchone()["phishing"]
        c.execute("SELECT COUNT(*) as spam FROM analysis_results WHERE user_id = ? AND risk_level = 'MEDIUM'", (user["id"],))
        spam = c.fetchone()["spam"]
        c.execute("SELECT COUNT(*) as high_risk FROM analysis_results WHERE user_id = ? AND risk_level = 'HIGH'", (user["id"],))
        high_risk = c.fetchone()["high_risk"]
        c.execute("SELECT COUNT(*) as legit FROM analysis_results WHERE user_id = ? AND risk_level = 'LOW'", (user["id"],))
        legit = c.fetchone()["legit"]
        
    return {
        "total_emails_scanned": total,
        "phishing_detected": phishing,
        "legitimate_emails": legit,
        "high_risk_emails": high_risk,
        "spam_emails": spam
    }

@app.get("/api/analysis/history")
def get_analysis_history(user: dict = Depends(get_current_user)):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM analysis_results WHERE user_id = ? ORDER BY analyzed_at DESC", (user["id"],))
        rows = c.fetchall()
        return [dict(row) for row in rows]

@app.get("/api/analysis/report/{report_id}")
def get_report(report_id: str, user: dict = Depends(get_current_user)):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM analysis_results WHERE id = ? AND user_id = ?", (report_id, user["id"]))
        row = c.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Report not found")
        return dict(row)

@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "healthy"}

@app.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    return {
        "model": "BERT",
        "model_type": "bert-base-uncased fine-tuned for phishing classification",
        "status": "loaded"
    }

@app.post("/predict", response_model=RiskResponse)
def predict(request: PredictionRequest):
    try:
        result = assess_email_risk(request.subject, request.body)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during prediction.")

class AnalyzeEmailRequest(BaseModel):
    message_id: str = None
    subject: str
    body: str
    sender: str = "Unknown Sender"
    recipient: str = None

@app.post("/api/analyze-email")
def analyze_and_save_email(req: AnalyzeEmailRequest, user: dict = Depends(get_current_user)):
    try:
        # Run BERT prediction and URL analysis
        result = assess_email_risk(req.subject, req.body)
        
        # Save to database
        result_id = str(uuid.uuid4())
        with get_db() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO analysis_results (id, user_id, message_id, subject, sender, prediction, 
phishing_probability, legitimate_probability, confidence, risk_level, urls_found)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result_id, user["id"], req.message_id, req.subject, req.sender, 
                result["prediction"], result["phishing_probability"], result["legitimate_probability"], 
                result["confidence"], result["risk_level"], result["urls_found"]
            ))
            conn.commit()
            
        result["success"] = True
        result["id"] = result_id
        result["subject"] = req.subject
        result["sender"] = req.sender
        
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during analysis.")
