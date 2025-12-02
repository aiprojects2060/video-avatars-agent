#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import mimetypes
import os
import shutil
from pathlib import Path

from google.genai import types

# Local storage configuration
# We use the same backend/files directory
BASE_DIR = Path(__file__).parent.parent / "backend" / "files"
BASE_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = "http://localhost:8000/files"

# Mock bucket name for Veo compatibility
ai_bucket_name = "local-bucket"

md5_hash = hashlib.md5()


async def upload_data_to_gcs(agent_id: str, data: bytes, mime_type: str) -> str:
    """
    Saves data to local filesystem instead of GCS.
    Returns a local URL.
    """
    file_hash = hashlib.md5(data).hexdigest()
    ext = mimetypes.guess_extension(mime_type) or ""
    if not ext and mime_type == 'image/jpeg':
        ext = '.jpg'
    file_name = f"{file_hash}{ext}"
    
    file_path = BASE_DIR / file_name
    with open(file_path, "wb") as f:
        f.write(data)
        
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import mimetypes
import os
import shutil
from pathlib import Path

from google.genai import types

# Local storage configuration
# We use the same backend/files directory
BASE_DIR = Path(__file__).parent.parent / "backend" / "files"
BASE_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = "http://localhost:8000/files"

# Mock bucket name for Veo compatibility
ai_bucket_name = "local-bucket"

md5_hash = hashlib.md5()


async def upload_data_to_gcs(agent_id: str, data: bytes, mime_type: str) -> str:
    """
    Saves data to local filesystem instead of GCS.
    Returns a local URL.
    """
    file_hash = hashlib.md5(data).hexdigest()
    ext = mimetypes.guess_extension(mime_type) or ""
    if not ext and mime_type == 'image/jpeg':
        ext = '.jpg'
    file_name = f"{file_hash}{ext}"
    
    file_path = BASE_DIR / file_name
    with open(file_path, "wb") as f:
        f.write(data)
        
    return f"{BASE_URL}/{file_name}"

def download_data_from_gcs(url: str) -> types.Blob:
    filename = url.split("/")[-1]
    file_path = BASE_DIR / filename
    
    if not file_path.exists():
         # Return empty blob or error
         return types.Blob(data=b"", mime_type="application/octet-stream")

    with open(file_path, "rb") as f:
        data = f.read()
        
    mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    
    return types.Blob(
        display_name=filename,
        data=data,
        mime_type=mime_type
    )