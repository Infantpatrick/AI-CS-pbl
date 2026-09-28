# Deployment Recommendation: AI-Based Email Phishing Detection

## 1. Resource Analysis
Based on the actual project files and dependencies, the following resource requirements have been identified:

- **Fine-Tuned BERT Model Size:** ~418 MB
- **Dependencies Size:** ~350 MB (assuming PyTorch CPU-only version is used via `torch --index-url https://download.pytorch.org/whl/cpu`). Full PyTorch would be ~2 GB.
- **Estimated RAM Requirement:** 800 MB - 1.2 GB
  - *Breakdown:* ~420 MB for the model weights in RAM, ~200 MB for PyTorch/FastAPI overhead, and an additional ~200 MB buffer for inference spikes and memory fragmentation.

## 2. Platform Comparison
Given the ~1 GB RAM requirement, standard free tiers for generic web apps (which typically limit RAM to 512 MB) will crash with Out Of Memory (OOM) errors during startup or inference.

- **Render (Paid):** The Starter tier (512 MB) is insufficient. The Standard tier ($25/mo, 2 GB RAM) would work smoothly but is costly for a student portfolio.
- **Railway:** Flexible billing based on usage. A 1-2 GB RAM instance would work and cost a few dollars a month.
- **AWS EC2:** A `t3.micro` (1 GB RAM, free tier) is extremely risky and prone to OOM. A `t3.small` (2 GB RAM) costs ~$15/mo.
- **Hugging Face Spaces (Docker):** The free tier ("CPU basic") provides 2 vCPUs and 16 GB RAM. It natively supports deploying arbitrary Docker containers (including FastAPI).

## 3. Recommended Platform: Hugging Face Spaces (Docker)
**Why it is suitable:**
- **Sufficient Resources:** The 16 GB RAM limit completely eliminates the OOM risks associated with generic free-tier web hosts.
- **Zero Cost:** Essential for a student portfolio project.
- **Minimal Changes:** By selecting the "Docker" SDK, we can deploy the existing FastAPI backend code and `Dockerfile` exactly as they are.
- **ML-Centric:** It is the industry standard for showcasing ML models and APIs.

## 4. Expected Limitations
- **Cold Starts:** Hugging Face Spaces may "sleep" after 48 hours of inactivity. The first request after a sleep period will take time to rebuild or load the container.
- **CPU Inference Only:** The free tier uses CPUs. Inference on long emails may take 1-3 seconds.
- **Ephemeral Storage:** Any data written to disk is lost upon restart (which aligns with our stateless API design).

## 5. Deployment Configuration & Steps
1. **Hugging Face Space Creation:** Create a new Space on Hugging Face, select **Docker** as the SDK.
2. **Dockerfile Updates:** Ensure the `Dockerfile` exposes the correct port (Hugging Face routes port 7860 by default, so we should map FastAPI to `7860`).
3. **Requirements Optimization:** Explicitly use the CPU version of PyTorch in `requirements.txt` to minimize container size and build time.
4. **Environment Variables:** No secret keys are strictly required for the core BERT inference, but CORS must be configured to allow the frontend's domain.

### Backend Start Command
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 7860
```

## 6. Security Considerations
- **No Secrets in Code:** Ensure no `.env` files or API keys are committed.
- **CORS:** The FastAPI app must configure CORS strictly if the frontend is hosted elsewhere (e.g., Vercel) so that only the frontend domain can make `POST /predict` requests.
- **Logging:** Do not log the contents of user-submitted emails in production to protect PII.
