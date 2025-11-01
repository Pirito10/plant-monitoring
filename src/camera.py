from datetime import datetime
from pathlib import Path
from picamera2 import Picamera2

def take_photo(out_dir="photos", width=1920, height=1080):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    picam = Picamera2()
    config = picam.create_still_configuration(
        main={"size": (width, height)}
    )
    picam.configure(config)
    picam.start()

    filepath = out / f"{datetime.now():%Y%m%d}.jpg"
    picam.capture_file(filepath)
    picam.stop()