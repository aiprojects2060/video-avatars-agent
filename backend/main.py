import sys
import os
import re
from typing import List

# Add root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Import the agent
try:
    from agents.video_avatar_agent.agent import root_agent
    from google.adk.models.llm_request import LlmRequest
    from google.genai import types
except ImportError as e:
    print(f"Error importing agent: {e}")
    sys.exit(1)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local files
app.mount("/files", StaticFiles(directory="backend/files"), name="files")

@app.post("/api/generate")
async def generate(prompt: str = Form(...), files: List[UploadFile] = File(...)):
    print(f"Received prompt: {prompt}")
    print(f"Received {len(files)} files")

    # Construct LlmRequest
    parts = [types.Part.from_text(text=prompt)]

    for file in files:
        content = await file.read()
        # We need to ensure mime_type is correct.
        # root_agent expects image/jpeg or similar.
        parts.append(types.Part.from_bytes(data=content, mime_type=file.content_type))

    request = LlmRequest(contents=[types.Content(parts=parts, role="user")])

    print("Invoking agent...")
    try:
        # Try async query if available, else sync
        if hasattr(root_agent, 'query_async'):
             response = await root_agent.query_async(request)
        else:
             response = root_agent.query(request)
             
        text = response.content or ""
        print(f"Agent response: {text}")
        
        # Extract URLs
        # Look for https://storage.mtls.cloud.google.com/... or similar
        # The agent is instructed to output https://...
        urls = re.findall(r'https?://[^\s<>"]+\.mp4', text)
        
        return {"videos": urls, "text": text}
    except Exception as e:
        print(f"Error invoking agent: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
