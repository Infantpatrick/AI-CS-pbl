# Phishing Detection Frontend

This is the React + Vite frontend for the AI-Based Email Phishing Detection project. It provides a modern, cybersecurity-themed dashboard to analyze emails using the FastAPI backend.

## Tech Stack
- React
- Vite
- Tailwind CSS
- Lucide React (Icons)
- Axios (API Client)

## Installation

```bash
cd frontend
npm install
```

## Environment Variables

Create a `.env` file in the `frontend` directory to specify the backend URL (defaults to `http://localhost:8000` if not set):

```env
VITE_API_URL=http://localhost:8000
```

## Running the Development Server

1. Ensure the FastAPI backend is running on port 8000.
2. Start the Vite dev server:

```bash
npm run dev
```

## Building for Production

To create an optimized production build:

```bash
npm run build
```

The output will be generated in the `dist/` directory.

## Features
- Real-time Email Classification Integration
- URL Extraction and Suspicious Indicator Display
- Confidence and Risk Assessment Visualization
- Premium Glassmorphism Dark Mode Design
- Smooth Animations and Responsive Layout
