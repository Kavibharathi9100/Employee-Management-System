from app.core.config import settings


def send_reset_email(to_email: str, reset_link: str):
    """
    Demo Email Service

    This function simulates sending an email.
    In production, integrate Gmail SMTP, Resend,
    SendGrid, Brevo, etc.
    """

    print("\n" + "=" * 60)
    print("PASSWORD RESET EMAIL")
    print("=" * 60)
    print(f"To      : {to_email}")
    print(f"From    : {settings.EMAIL_USERNAME}")
    print("Subject : Reset Your Password")
    print("-" * 60)
    print("Reset Link:")
    print(reset_link)
    print("=" * 60)
    print("Demo Email Sent Successfully")
    print("=" * 60 + "\n")

    return {
        "status": "success",
        "message": "Password reset email simulated successfully"
    }