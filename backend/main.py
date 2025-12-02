import sys
import os
from typing import List

# Add root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Import the lightweight agent logic
from backend.agent_logic import process_request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local files
# Ensure directory exists
os.makedirs("backend/files", exist_ok=True)
app.mount("/files", StaticFiles(directory="backend/files"), name="files")

@app.post("/api/generate")
async def generate(prompt: str = Form(...), files: List[UploadFile] = File(...)):
    print(f"Received prompt: {prompt}")
    print(f"Received {len(files)} files")

    # Save files locally (or mock processing them)
    # In Vercel, local filesystem is ephemeral, but okay for a single request lifecycle.
    # We need to save them to pass URLs/paths to the agent logic.
    saved_file_urls = []
    for file in files:
        # Simple save to backend/files
        file_path = os.path.join("backend/files", file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        # In Vercel, we can't easily serve these back via StaticFiles if they are created at runtime 
        # unless we use /tmp and serve from there, but StaticFiles expects a fixed dir.
        # For the mock agent, we just need the list of "urls" (paths).
        # We'll use relative paths.
        saved_file_urls.append(f"/files/{file.filename}")

    print("Invoking agent...")
    try:
        result = await process_request(prompt, saved_file_urls)
        return result
    except Exception as e:
        print(f"Error invoking agent: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
