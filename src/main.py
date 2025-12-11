from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import load_config
from src.camera import take_photo
from src.moisture_sensor import read_soil_moisture

cfg = load_config()

scheduler = BlockingScheduler()

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
    raw, voltage = read_soil_moisture()
    print(f"Humedad suelo -> Raw: {raw}, Voltaje: {voltage:.4f} V")

scheduler.add_job(
    job_read_moisture,
    "interval",
    seconds=10
)

scheduler.start()