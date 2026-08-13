from flask import (
    render_template,
    current_app
)

from services.sandbox_service import (
    SandboxService
)

from services.email_queue_service import (
    EmailQueueService
)


class EmailService:

    @staticmethod
    def send_reset_email(user):

        if SandboxService.is_enabled():

            return {
                "status": "sandbox",
                "message": (
                    f"Password reset email "
                    f"suppressed for {user.email}"
                )
            }

        token = user.generate_reset_token()

        reset_link = (
            f"{current_app.config.get('BASE_URL', '')}"
            f"/auth/reset-password/{token}"
        )

        body = render_template(
            "email/password_reset.html",
            user=user,
            reset_link=reset_link
        )

        return EmailQueueService.queue_email(
            recipients=[user.email],
            subject="Password Reset",
            body=body,
            email_type="PASSWORD_RESET"
        )