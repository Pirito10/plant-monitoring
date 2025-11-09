import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_config():
    path = Path("config.yaml")
    
    with path.open("r") as f:
        return yaml.safe_load(f)