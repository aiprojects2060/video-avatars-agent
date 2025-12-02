# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import json
import logging
import mimetypes
import time
from typing import Literal, Optional
import uuid

from google.adk.models.google_llm import Gemini

from google.genai import types

from media_models import MediaAsset
from storage_utils import ai_bucket_name

OPERATION_WAIT_TIME = 10.0 # 10 seconds between operation status check
AUTHORIZED_URI = "https://storage.mtls.cloud.google.com/"


async def generate_video(
    prompt: str,
    start_frame_image_gsc_uri: Optional[str] = None,
    end_frame_image_gsc_uri: Optional[str] = None,
    video_duration_seconds: int = 8,
    aspect_ratio: Literal["16:9", "9:16"] = "16:9",
) -> MediaAsset:
    """Generates a video using Veo 3 model (MOCKED for local run)."""
    
    agent_name = "mcp-tool"
    invocation = uuid.uuid4().hex
    
    logging.info(f"[{invocation}] Generating a video (MOCKED).")
    
    # Mock delay
    await asyncio.sleep(2)
    
    # Return a dummy video URL (local)
    # Ensure this file exists in backend/files
    dummy_video_url = "http://localhost:8001/files/sample_video.mp4"
    
    result_media = MediaAsset(uri=dummy_video_url)
    
    logging.info(
        f"[{invocation}] Video Generation result:\n{result_media.model_dump_json(indent=2)}"
    )
    return result_media


