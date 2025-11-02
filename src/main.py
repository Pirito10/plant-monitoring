import time
from apscheduler.schedulers.background import BackgroundScheduler

from src.camera import take_photo

scheduler = BackgroundScheduler()
scheduler.add_job(take_photo, "cron", hour="10,18")
scheduler.start()

try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    scheduler.shutdown()