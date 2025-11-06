import yaml
from pathlib import Path

def load_config():
    path = Path("config.yaml")
    
    with path.open("r") as f:
        return yaml.safe_load(f)