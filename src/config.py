import yaml
from pathlib import Path

# Definimos el directorio base del sistema
BASE_DIR = Path(__file__).resolve().parent.parent

# Función para cargar la configuración del sistema
def load_config():
    # Ruta al fichero de configuración
    path = BASE_DIR / "config.yaml"
    
    # Abrimos y leemos el fichero YAML
    with path.open("r") as f:
        return yaml.safe_load(f)