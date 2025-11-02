from apscheduler.schedulers.blocking import BlockingScheduler

from src.camera import take_photo

scheduler = BlockingScheduler()
scheduler.add_job(take_photo, "cron", hour="10,18")
scheduler.start()