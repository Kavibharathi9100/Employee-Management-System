from celery import shared_task
  
from app.services.email_service import send_reset_email


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=10
)
def send_reset_email_task(
    self,
    email: str,
    reset_link: str
):
    try:
        send_reset_email(
            email,
            reset_link
        )

    except Exception as exc:
        raise self.retry(exc=exc)


