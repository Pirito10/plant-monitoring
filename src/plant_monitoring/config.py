import yaml

from plant_monitoring.paths import BASE_DIR

# Función para cargar la configuración del sistema
def load_config():
    # Ruta al fichero de configuración
    path = BASE_DIR / "settings.yaml"

    # Abrimos y leemos el fichero YAML
    with path.open("r") as f:
        return yaml.safe_load(f)
