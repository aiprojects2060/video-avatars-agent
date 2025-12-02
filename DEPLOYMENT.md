# Video Avatar Agent - Deployment Guide

## Frontend Deployment (Vercel)

The **frontend** is deployed on Vercel and shows a working demo with mock video generation.

To deploy:
1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect the Next.js frontend
3. The frontend will work with mock data

## Backend Deployment (Separate)

The **Python backend** should be deployed separately on platforms like:
- **Google Cloud Run** (recommended for Google Cloud integration)
- **Railway**
- **Render**
- **Fly.io**

### Backend Setup

1. Navigate to the `backend/` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   ```
   GOOGLE_API_KEY=your_api_key
   GOOGLE_CLOUD_PROJECT=your_project
   ```
4. Run: `python main.py`

### Connecting Frontend to Backend

Once your backend is deployed, update `frontend/src/app/page.tsx` to call your backend URL instead of the mock data.

## Why This Architecture?

Vercel Serverless Functions have a 250MB size limit. Google Cloud Python SDKs exceed this limit, so we:
- Deploy the **lightweight Next.js frontend** on Vercel
- Deploy the **Python backend** on a platform designed for Python apps
- This gives you the best of both worlds: fast global CDN for frontend + powerful backend
