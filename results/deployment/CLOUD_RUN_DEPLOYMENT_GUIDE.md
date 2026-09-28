# Google Cloud Run Deployment Guide

This guide describes how to deploy the AI-Based Email Phishing Detection API (FastAPI backend + BERT model) to Google Cloud Run. 

## 1. Google Cloud Setup

1. **Create or select a Google Cloud Project**:
   ```bash
   gcloud config set project [YOUR_PROJECT_ID]
   ```
2. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   ```
3. **Configure Docker for Artifact Registry**:
   ```bash
   gcloud auth configure-docker [REGION]-docker.pkg.dev
   ```

## 2. Required APIs

Ensure the following APIs are enabled in your Google Cloud Project:
- **Cloud Run API**: `run.googleapis.com`
- **Artifact Registry API**: `artifactregistry.googleapis.com`
- **Cloud Build API**: `cloudbuild.googleapis.com` (if building in the cloud)

You can enable them using the CLI:
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

## 3. Docker/Build Configuration

The deployment uses a Docker container.
- **Dockerfile**: Configured to use a lightweight Python 3.9 image. It copies the `models/` directory (which contains the fine-tuned BERT model, ~418 MB) into the container and installs dependencies from `requirements.txt`.
- **.dockerignore**: Excludes unnecessary directories like `data/`, `frontend/`, `venv/`, and `results/` to keep the image lean.
- **Requirements**: Contains `fastapi`, `uvicorn`, `torch`, `transformers`, `httpx`, and `pydantic`.
- **Production Start Command**: `CMD exec uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-8080}` (Supports Cloud Run's `$PORT` environment variable).

To build and push the container to Artifact Registry (assuming a repository named `aics-repo` exists):
```bash
# 1. Create Artifact Registry Repository (if not exists)
gcloud artifacts repositories create aics-repo --repository-format=docker --location=[REGION]

# 2. Build and Tag the Image
docker build -t [REGION]-docker.pkg.dev/[YOUR_PROJECT_ID]/aics-repo/phishing-api:latest .

# 3. Push to Artifact Registry
docker push [REGION]-docker.pkg.dev/[YOUR_PROJECT_ID]/aics-repo/phishing-api:latest
```

## 4. Deployment Command

Deploy to Cloud Run using the pushed image:

```bash
gcloud run deploy phishing-api \
  --image [REGION]-docker.pkg.dev/[YOUR_PROJECT_ID]/aics-repo/phishing-api:latest \
  --region [REGION] \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --concurrency 50
```

## 5. Recommended Resources

- **Recommended Memory**: `2Gi` (2 GB). The BERT model takes ~418 MB on disk and requires roughly 800 MB - 1.2 GB of RAM when loaded by PyTorch. Setting the limit to 2 GB provides sufficient headroom.
- **Recommended CPU**: `1` (or `2` if higher throughput is needed). Since we are doing CPU inference with PyTorch, at least 1 full vCPU is required.

## 6. Environment Variables

No special environment variables are strictly required by the code. Cloud Run automatically injects the `PORT` environment variable, which the application uses to bind the server.

## 7. How to Obtain the Live URL

After running the deployment command, Cloud Run will output a Service URL. You can also retrieve it anytime using:
```bash
gcloud run services describe phishing-api --platform managed --region [REGION] --format 'value(status.url)'
```

## 8. How to Test the API

Once deployed, you can test the endpoints against your live URL (`[SERVICE_URL]`).

### Test `/health`
Check if the API is running correctly.
```bash
curl -X GET [SERVICE_URL]/health
```
**Expected Response**: `{"status": "healthy"}`

### Test `/model-info`
Verify the model is loaded properly.
```bash
curl -X GET [SERVICE_URL]/model-info
```
**Expected Response**: Information about the loaded BERT model.

### Test `/predict`
Run an email subject and body through the model.
```bash
curl -X POST [SERVICE_URL]/predict \
  -H "Content-Type: application/json" \
  -d '{"subject": "Urgent: Update your account details", "body": "Click here to update: http://suspicious.link"}'
```
**Expected Response**: A JSON object containing `prediction`, `risk_level`, `confidence`, and URL analysis results.
