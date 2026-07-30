from app.celery.tasks import send_reset_email_task

send_reset_email_task.delay(
    "your_email@gmail.com",
    "https://example.com/reset-password"
)

print("Task Added Successfully")