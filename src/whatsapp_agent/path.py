from pathlib import Path
import sys 
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SRC_DIR = PROJECT_ROOT / "src"
PROJECT_DIR = SRC_DIR / "whatsapp_agent"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
    
load_dotenv (PROJECT_ROOT / "example.env")

SESSION_DIR = Path.home() / ".whatsapp_session"
SESSION_DIR.mkdir(parents=True, exist_ok=True)

