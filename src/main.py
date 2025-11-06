from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import load_config
from src.camera import take_photo

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
scheduler.start()