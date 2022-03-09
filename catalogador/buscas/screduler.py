from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import backports.zoneinfo as zoneinfo
from buscas import cron


BR = zoneinfo.ZoneInfo("America/Sao_Paulo")


def extracts():
    print(f'Executando preparação de Scheduler')
    scheduler = BackgroundScheduler(timezone=BR)

    now = datetime.today() + timedelta(seconds=120)
    tomorow = now + timedelta(days=1)
    scheduler.add_job(cron.ResetValues, 'cron', hour=now.hour, minute=now.minute, day=now.day, year=now.year, end_date=tomorow.__str__()[:10]+' 00:00:00.000000')

    scheduler.add_job(cron.extract_1_1_Django, 'cron', day_of_week='0,1,2,3,4', hour=14, minute=0)
    scheduler.add_job(cron.all_dairly_task, 'cron', day_of_week='1,2,3,4,5', hour=0, minute=1)
    scheduler.start()
