from datetime import datetime
from picamera2 import Picamera2

# Función para tomar una foto con la cámara de la Raspberry Pi
def take_photo(photos_dir, width, height):
    # Creamos el directorio de salida si no existe
    photos_dir.mkdir(parents=True, exist_ok=True)

    # Inicializamos y configuramos la cámara
    with Picamera2() as picam:
        config = picam.create_still_configuration(
            main={"size": (width, height)}
        )
        picam.configure(config)
        picam.start()

        # Fichero de salida de la imagen
        filepath = photos_dir / f"{datetime.now():%Y-%m-%d_%H-%M}.jpg"
        # Tomamos la foto
        picam.capture_file(filepath)

        # Detenemos la cámara
        picam.stop()
