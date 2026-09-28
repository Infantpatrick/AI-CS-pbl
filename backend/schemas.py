from pydantic import BaseModel, Field, root_validator
from typing import List, Optional

class PredictionRequest(BaseModel):
    subject: str = Field(..., max_length=1000, description="The subject of the email")
    body: str = Field(..., max_length=50000, description="The body of the email")

    @root_validator(pre=True)
    def check_not_both_empty(cls, values):
        subject = values.get("subject", "")
        body = values.get("body", "")
        
        if isinstance(subject, str):
            subject = subject.strip()
        if isinstance(body, str):
            body = body.strip()
            
        if not subject and not body:
            raise ValueError("Both subject and body cannot be empty.")
        return values

class RiskResponse(BaseModel):
    prediction: str
    phishing_probability: float
    legitimate_probability: float
    confidence: float
    risk_level: str
    urls_found: int
    extracted_urls: List[str] = []
    url_indicators: List[str]
    risk_reasons: List[str]

class HealthResponse(BaseModel):
    status: str

class ModelInfoResponse(BaseModel):
    model: str
    model_type: str
    status: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    has_gmail: Optional[bool] = False
