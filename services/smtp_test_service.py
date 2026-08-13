import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from models.system_settings import (
    SystemSettings
)

from services.logger import logger


class SMTPTestService:

    @staticmethod
    def get_settings():

        settings = (
            SystemSettings.query.first()
        )

        if not settings:

            raise Exception(
                "System settings not configured."
            )

        if not settings.smtp_server:

            raise Exception(
                "SMTP server not configured."
            )

        return settings

    @staticmethod
    def test_connection(
        recipient_email
    ):

        settings = (
            SMTPTestService.get_settings()
        )

        msg = MIMEMultipart()

        msg["From"] = (

            f"{settings.smtp_sender_name} "
            f"<{settings.smtp_sender_address}>"

        )

        msg["To"] = recipient_email

        msg["Subject"] = (
            "SMTP Test Message"
        )

        body = """
        This is a test email generated
        by the Laboratory Forms System.

        If you received this email,
        SMTP configuration is working
        correctly.
        """

        msg.attach(
            MIMEText(body, "plain")
        )

        try:

            server = smtplib.SMTP(

                settings.smtp_server,

                settings.smtp_port

            )

            server.ehlo()

            if getattr(
                settings,
                "smtp_use_tls",
                False
            ):

                server.starttls()

                server.ehlo()

            if settings.smtp_username:

                server.login(

                    settings.smtp_username,

                    settings.smtp_password

                )

            server.sendmail(

                settings.smtp_sender_address,

                [recipient_email],

                msg.as_string()

            )

            server.quit()

            logger.info(
                "SMTP test successful"
            )

            return {

                "success": True,

                "message":
                "SMTP test email sent."

            }

        except Exception as ex:

            logger.exception(
                "SMTP test failed"
            )

            raise Exception(

                f"SMTP test failed: "
                f"{str(ex)}"

            )

    @staticmethod
    def validate_configuration():

        settings = (
            SMTPTestService.get_settings()
        )

        errors = []

        if not settings.smtp_server:

            errors.append(
                "SMTP server missing."
            )

        if not settings.smtp_port:

            errors.append(
                "SMTP port missing."
            )

        if not settings.smtp_sender_address:

            errors.append(
                "SMTP sender address missing."
            )

        return {

            "valid":
            len(errors) == 0,

            "errors":
            errors

        }

    @staticmethod
    def connectivity_test():

        settings = (
            SMTPTestService.get_settings()
        )

        try:

            server = smtplib.SMTP(

                settings.smtp_server,

                settings.smtp_port,

                timeout=10

            )

            server.ehlo()

            server.quit()

            return {

                "success": True,

                "server":
                settings.smtp_server,

                "port":
                settings.smtp_port

            }

        except Exception as ex:

            return {

                "success": False,

                "error":
                str(ex)

            }

    @staticmethod
    def server_capabilities():

        settings = (
            SMTPTestService.get_settings()
        )

        try:

            server = smtplib.SMTP(

                settings.smtp_server,

                settings.smtp_port,

                timeout=10

            )

            server.ehlo()

            capabilities = dict(
                server.esmtp_features
            )

            server.quit()

            return {

                "success": True,

                "capabilities":
                capabilities

            }

        except Exception as ex:

            return {

                "success": False,

                "error":
                str(ex)

            }