# Deployment Report

## Configuration
- **Platform**: Hugging Face Spaces
- **Space SDK**: Docker
- **Backend Framework**: FastAPI + Uvicorn
- **Required Hardware**: CPU basic (16GB RAM, 2 vCPU) - Free Tier
- **Model Size**: ~418 MB
- **Space URL**: *Pending Account Setup*

## Deployment Checklist & Verification
- [x] **Model Size Confirmed**: ~418 MB
- [x] **Dependencies Optimized**: PyTorch CPU is required
- [x] **Dockerfile**: Configured to expose Port 7860
- [x] **.dockerignore**: Excludes datasets, venv, cache, and frontend build
- [ ] **Live Space Creation**: Pending user action

## Manual Deployment Steps for Hugging Face Spaces

1. Create or login to a [Hugging Face account](https://huggingface.co/).
2. Click on **New Space** from your profile dropdown.
3. Enter a Space name (e.g., `phishing-detection-api`).
4. Select **Docker** as the Space SDK and choose the **Blank** template.
5. Select the **CPU basic - 16GB · 2 vCPU · Free** hardware tier (this is more than enough for our ~800MB–1.2GB RAM requirement).
6. Click **Create Space**.
7. Connect your space to this repository via Git, or upload the following files directly via the browser interface:
   - `Dockerfile`
   - `requirements.txt`
   - `backend/app.py`
   - `backend/schemas.py`
   - `src/` (the entire source code directory for processing)
   - `models/bert_phishing/` (the entire fine-tuned model directory)
8. The Space will automatically build the Docker image and start the FastAPI server.
9. Obtain your public Space URL (e.g., `https://username-phishing-detection-api.hf.space`).

## Next Steps
Provide the public Space URL once the Space is running. We will then execute the final Live API Verification (Step 5) and Security & Performance measurements.
