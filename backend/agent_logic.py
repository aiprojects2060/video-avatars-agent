import os
import json
import asyncio
from typing import List, Optional
from pydantic import BaseModel
from google import genai
from google.genai import types

# Mock video generation
async def generate_video_mock(prompt: str, image_url: str) -> str:
    # In a real app, this would call Veo API
    # Here we return a dummy URL. 
    # Note: In Vercel, localhost URLs won't work for the client if the client is external,
    # but here the client is the frontend served from the same origin.
    # However, for Vercel deployment, we should return a relative path or a public URL.
    # Since we are mocking, we'll return a relative path that the frontend can resolve.
    await asyncio.sleep(1)
    return "/files/sample_video.mp4"

class ScriptChunk(BaseModel):
    chunk_id: int
    script_chunk: str
    view_index: int
    estimated_duration: int

class ScriptSequence(BaseModel):
    chunks: List[ScriptChunk]

async def process_request(user_prompt: str, file_urls: List[str]):
    # Initialize client
    # Try to use API Key if available, otherwise Vertex AI default creds
    api_key = os.environ.get("GOOGLE_API_KEY")
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if api_key:
        client = genai.Client(api_key=api_key)
    elif project:
        client = genai.Client(vertexai=True, project=project, location=location)
    else:
        # Fallback for local testing without explicit config
        print("Warning: No GOOGLE_API_KEY or GOOGLE_CLOUD_PROJECT found.")
        client = None

    # 1. Script Sequencer
    if client:
        sequencer_prompt = f"""
        You are a professional video editor.
        Task:
        1. Split the following script/request into 8-second chunks.
        2. Assign a view index (1-4) to each chunk.
        
        Input Script/Request:
        {user_prompt}
        
        Output JSON format:
        {{
            "chunks": [
                {{ "chunk_id": 1, "script_chunk": "...", "view_index": 1, "estimated_duration": 8 }}
            ]
        }}
        """
        
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp", # Use a fast model
                contents=sequencer_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ScriptSequence
                )
            )
            sequence_data = response.parsed
        except Exception as e:
            print(f"Error in sequencer: {e}")
            # Fallback
            sequence_data = ScriptSequence(chunks=[
                ScriptChunk(chunk_id=1, script_chunk=user_prompt, view_index=1, estimated_duration=8)
            ])
    else:
        # Mock sequencer if no client
        sequence_data = ScriptSequence(chunks=[
            ScriptChunk(chunk_id=1, script_chunk=user_prompt, view_index=1, estimated_duration=8)
        ])

    # 2. Video Generation Loop
    results = []
    if not sequence_data or not sequence_data.chunks:
         sequence_data = ScriptSequence(chunks=[
            ScriptChunk(chunk_id=1, script_chunk=user_prompt, view_index=1, estimated_duration=8)
        ])

    for chunk in sequence_data.chunks:
        # Select image (1-based index to 0-based)
        if file_urls:
            img_idx = (chunk.view_index - 1) % len(file_urls)
            image_url = file_urls[img_idx]
        else:
            image_url = ""
        
        video_prompt = f"{user_prompt} . Scene: {chunk.script_chunk}"
        
        video_url = await generate_video_mock(video_prompt, image_url)
        results.append(video_url)
        
    return {"videos": results, "text": json.dumps([c.model_dump() for c in sequence_data.chunks])}
