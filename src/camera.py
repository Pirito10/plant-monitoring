from datetime import datetime
from picamera2 import Picamera2

from src.config import BASE_DIR

# Función para tomar una foto con la cámara de la Raspberry Pi
def take_photo(out_dir, width, height):
    # Creamos el directorio de salida si no existe
    out_dir = BASE_DIR / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # Inicializamos y configuramos la cámara
    picam = Picamera2()
    config = picam.create_still_configuration(
        main={"size": (width, height)}
    )
    picam.configure(config)
    picam.start()

    # Fichero de salida de la imagen
    filepath = out_dir / f"{datetime.now():%Y-%m-%d_%H-%M}.jpg"
    # Tomamos la foto
    picam.capture_file(filepath)
    # Detenemos y cerramos la cámara
    picam.stop()
    picam.close()