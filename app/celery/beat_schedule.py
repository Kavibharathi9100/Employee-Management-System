from celery.schedules import crontab

from app.celery.celery_app import celery_app


celery_app.conf.beat_schedule = {

    "attendance-report": {

        "task": "app.celery.tasks.daily_attendance",

        "schedule": crontab(
            hour=18,
            minute=0
        ),
    }

}