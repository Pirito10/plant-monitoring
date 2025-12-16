from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import load_config
from src.camera import take_photo
from src.moisture_sensor import read_soil_moisture
from src.led_rgb import update_led

# Cargamos la configuración
cfg = load_config()

# Creamos el planificador de tareas
scheduler = BlockingScheduler()

# Programamos la toma de fotos
scheduler.add_job(
    take_photo,
    "cron",
    hour=",".join(map(str, cfg["scheduler"]["hours"])),
    args=[
        cfg["paths"]["photos"],
        cfg["camera"]["width"],
        cfg["camera"]["height"]
    ],
)

#! Temporal
def job_read_moisture():
    moisture = read_soil_moisture(cfg["moisture"]["raw_dry"], cfg["moisture"]["raw_wet"])
    update_led(moisture, 50)
    print(f"Humedad suelo: {moisture:5.1f}%")

# Programamos la lectura del sensor de humedad
scheduler.add_job(
    job_read_moisture,
    "interval",
    seconds=10
)

# Iniciamos el planificador
scheduler.start()