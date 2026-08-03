import resend

from app.core.config import settings

# Set API Key
resend.api_key = settings.RESEND_API_KEY


def send_reset_email(to_email: str, reset_link: str):
    """
    Send password reset email using Resend.
    """

    try:
        resend.Emails.send({
            "from": settings.FROM_EMAIL,
            "to": to_email,
            "subject": "Reset Your Password",
            "html": f"""
            <h2>Password Reset Request</h2>

            <p>Hello,</p>

            <p>You requested to reset your password.</p>

            <p>
                <a href="{reset_link}"
                   style="
                       background:#2563eb;
                       color:white;
                       padding:12px 20px;
                       text-decoration:none;
                       border-radius:6px;
                   ">
                    Reset Password
                </a>
            </p>

            <p>Or copy and paste this link into your browser:</p>

            <p>{reset_link}</p>

            <p>This link expires in 15 minutes.</p>

            <br>

            <p>Regards,</p>
            <p>HRMS Team</p>
            """
        })

        return {
            "status": "success",
            "message": "Password reset email sent successfully"
        }

    except Exception as e:
        print("Resend Error:", e)
        raise e