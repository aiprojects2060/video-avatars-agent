import hashlib
import mimetypes
import os
import shutil
from pathlib import Path

# Local storage configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent / "backend" / "files"
BASE_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = "http://localhost:8001/files"

md5_hash = hashlib.md5()

async def upload_data_to_gcs(agent_id: str, data: bytes, mime_type: str) -> str:
    """
    Saves data to local filesystem instead of GCS.
    Returns a local URL.
    """
    # Create a hash of the content to use as filename
    file_hash = hashlib.md5(data).hexdigest()
    
    # Determine extension
    ext = mimetypes.guess_extension(mime_type) or ""
    if not ext and mime_type == 'image/jpeg':
        ext = '.jpg'
        
    file_name = f"{file_hash}{ext}"
    
    # Save file locally
    file_path = BASE_DIR / file_name
    with open(file_path, "wb") as f:
        f.write(data)
        
    # Return local URL
    # Note: agent_id is ignored in flat local structure for simplicity, 
    # or could be used as a subdir if needed.
    return f"{BASE_URL}/{file_name}"

def download_data_from_gcs(url: str) -> bytes:
    """
    Reads data from local filesystem.
    URL is expected to be http://localhost:8001/files/...
    """
    filename = url.split("/")[-1]
    file_path = BASE_DIR / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    with open(file_path, "rb") as f:
        data = f.read()
        
    return data