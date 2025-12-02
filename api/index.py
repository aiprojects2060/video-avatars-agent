import sys
import os

# Add the current directory to sys.path so that 'backend' and 'agents' can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.main import app
