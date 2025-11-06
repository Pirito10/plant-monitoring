from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import load_config
from src.camera import take_photo

cfg = load_config()

scheduler = BlockingScheduler()
scheduler.add_job(take_photo, "cron", hour="10,18")
scheduler.start()