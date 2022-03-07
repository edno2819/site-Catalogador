from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import backports.zoneinfo as zoneinfo
from buscas import cron


BR = zoneinfo.ZoneInfo("America/Sao_Paulo")


def extracts():
    now = datetime.today() + timedelta(seconds=120)
    tomorow = now + timedelta(days=1)
    scheduler = BackgroundScheduler(timezone=BR)
    #scheduler.add_job(cron.ResetValues, 'cron', hour=now.hour, minute=now.minute, day=now.day, year=now.year, end_date=tomorow.__str__()[:10])
    scheduler.add_job(cron.extract_1_1_Django, 'cron', day_of_week='1,2,3,4,5', hour=14, minute=0)
    scheduler.add_job(cron.all_dairly_task, CronTrigger.from_crontab('1 0 * * 2,3,4,5,6'))
    scheduler.start()