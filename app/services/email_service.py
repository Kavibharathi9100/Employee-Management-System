import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def send_reset_email(to_email: str, reset_link: str):
    """
    Sends password reset email using Gmail App Password.
    """

    message = MIMEMultipart()

    message["From"] = settings.EMAIL_USERNAME
    message["To"] = to_email
    message["Subject"] = "Reset Your Password"

    body = f"""
Hello,

You requested to reset your password.

Click the link below to reset your password:

{reset_link}

This link will expire in 15 minutes.

If you did not request this, please ignore this email.

Regards,
Employee Management System
"""

    message.attach(MIMEText(body, "plain"))

    try:
        print("========== EMAIL CONFIG ==========")
        print("EMAIL_USERNAME:", settings.EMAIL_USERNAME)
        print("SMTP_SERVER:", settings.SMTP_SERVER)
        print("SMTP_PORT:", settings.SMTP_PORT)
        print("==================================")

        # Gmail SSL Connection
        with smtplib.SMTP_SSL(
            settings.SMTP_SERVER,
            settings.SMTP_PORT
        ) as smtp:

            smtp.login(
                settings.EMAIL_USERNAME,
                settings.EMAIL_PASSWORD
            )

            smtp.send_message(message)

        print("✅ Password reset email sent successfully.")

    except Exception as e:
        print("❌ Email Error:", str(e))
        raise