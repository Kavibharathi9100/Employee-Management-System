import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def send_reset_email(to_email: str, reset_link: str):
    message = MIMEMultipart()

    message["From"] = settings.FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = "Reset Your Password"

    body = f"""
Hello,

Click the link below to reset your password.

{reset_link}

This link expires in 15 minutes.

HRMS Team
"""

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()

        server.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD
        )

        server.send_message(message)

    print("Email sent successfully")