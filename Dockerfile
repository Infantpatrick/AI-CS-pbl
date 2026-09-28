# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn httpx

# Copy the rest of the application code
COPY backend/ backend/
COPY src/ src/
COPY models/ models/

# Expose port 8080 (default for Cloud Run)
EXPOSE 8080

# Run uvicorn when the container launches, binding to 0.0.0.0 and PORT
CMD exec uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-8080}
