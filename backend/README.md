# Backend API

This directory contains the FastAPI backend for the Phishing Detection application.

## Architecture

- **FastAPI**: Provides the REST API endpoints.
- **Pydantic**: Validates input requests and structures the JSON responses.
- **Risk Assessment**: Uses the existing Phase 12 logic to combine ML predictions with static URL analysis.
- **Model**: Uses the fine-tuned BERT model (Phase 10) loaded at startup.

## Endpoints

- `GET /health` : Returns the health status of the API.
- `GET /model-info` : Returns basic information about the loaded model.
- `POST /predict` : Accepts an email (subject + body) and returns the full risk assessment.

## Running the Server

Use `uvicorn` to start the backend server:

```bash
uvicorn backend.app:app --reload
```
