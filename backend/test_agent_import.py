import sys
import os

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from agents.video_avatar_agent.agent import root_agent
    print("Successfully imported root_agent")
    print(f"Type: {type(root_agent)}")
    print(f"Dir: {dir(root_agent)}")
except Exception as e:
    print(f"Error importing root_agent: {e}")
