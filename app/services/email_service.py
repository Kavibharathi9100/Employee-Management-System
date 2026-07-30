import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from xmlrpc import server

from app.core.config import settings

def send_reset_email(to_email: str, reset_link: str):
    message = MIMEMultipart()

    message["From"] = settings.EMAIL_USERNAME
    message["To"] = to_email
    message["Subject"] = "Reset Your Password"

    body = f"""
Hello,

Click the link below to reset your password.

{reset_link}

This link expires in 15 minutes.

Thank you,
HR Team
"""

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            print("EMAIL_USERNAME:", settings.EMAIL_USERNAME)
            print("EMAIL_PASSWORD:", settings.EMAIL_PASSWORD)
            print("SMTP_SERVER:", settings.SMTP_SERVER)
            print("SMTP_PORT:", settings.SMTP_PORT)
            server.login(
                settings.EMAIL_USERNAME,
                settings.EMAIL_PASSWORD
            )
            server.send_message(message)

    except Exception as e:
        print("Email Error:", e)
        raise e


