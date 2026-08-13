import os
import smtplib

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

from flask import render_template

from extensions import db

from models.email_queue import EmailQueue
from models.settings import SystemSettings

from services.logger import logger


class EmailQueueService:

    @staticmethod
    def get_settings():

        settings = (
            SystemSettings.query.first()
        )

        if not settings:

            raise Exception(
                "SMTP settings not configured."
            )

        return settings

    @staticmethod
    def queue_email(
        recipients,
        subject,
        body,
        attachments=None,
        submission_id=None,
        email_type="GENERAL"
    ):

        if attachments is None:
            attachments = []

        queue_item = EmailQueue(

            submission_id=submission_id,

            recipients=recipients,

            subject=subject,

            body=body,

            attachments=attachments,

            email_type=email_type,

            status="PENDING",

            retry_count=0,

            recipient_count=len(recipients),

            attachment_count=len(
                attachments
            )

        )

        db.session.add(
            queue_item
        )

        db.session.commit()

        logger.info(

            f"Queued email "
            f"{queue_item.id}"

        )

        return queue_item.id

    @staticmethod
    def queue_submission_email(
        submission
    ):

        recipients = []

        if submission.results_emails:

            recipients.extend(
                submission.results_emails
            )

        if not recipients:

            raise Exception(
                "No recipients configured."
            )

        subject = (

            f"Results - "
            f"{submission.sample_number}"

        )

        body = render_template(

            "email/submission_complete.html",

            submission=submission

        )

        attachments = []

        if submission.pdf_file:

            attachments.append(
                submission.pdf_file
            )

        if submission.csv_file:

            attachments.append(
                submission.csv_file
            )

        return (

            EmailQueueService.queue_email(

                recipients=recipients,

                subject=subject,

                body=body,

                attachments=
                attachments,

                submission_id=
                submission.id,

                email_type=
                "SUBMISSION"

            )

        )

    @staticmethod
    def send(email_queue):

        settings = (
            EmailQueueService
            .get_settings()
        )

        msg = MIMEMultipart()

        msg["From"] = (

            f"{settings.smtp_sender_name} "

            f"<{settings.smtp_sender_address}>"

        )

        msg["To"] = ", ".join(
            email_queue.recipients
        )

        msg["Subject"] = (
            email_queue.subject
        )

        msg.attach(

            MIMEText(

                email_queue.body,

                "html"

            )

        )

        attachments = (
            email_queue.attachments
            or []
        )

        for file_path in attachments:

            if not os.path.exists(
                file_path
            ):
                logger.warning(

                    f"Attachment missing: "

                    f"{file_path}"

                )

                continue

            with open(
                file_path,
                "rb"
            ) as attachment:

                part = MIMEBase(
                    "application",
                    "octet-stream"
                )

                part.set_payload(
                    attachment.read()
                )

            encoders.encode_base64(
                part
            )

            filename = (
                os.path.basename(
                    file_path
                )
            )

            part.add_header(

                "Content-Disposition",

                f'attachment; '
                f'filename="{filename}"'

            )

            msg.attach(part)

        try:

            server = smtplib.SMTP(

                settings.smtp_server,

                settings.smtp_port

            )

            if settings.smtp_use_tls:

                server.starttls()

            if settings.smtp_username:

                server.login(

                    settings.smtp_username,

                    settings.smtp_password

                )

            server.sendmail(

                settings.smtp_sender_address,

                email_queue.recipients,

                msg.as_string()

            )

            server.quit()

            logger.info(

                f"Email sent: "

                f"{email_queue.id}"

            )

            return "SMTP Accepted"

        except Exception as ex:

            logger.exception(
                "SMTP send failed"
            )

            raise ex

    @staticmethod
    def get_stats():

        return {

            "pending":

                EmailQueue.query
                .filter_by(
                    status="PENDING"
                )
                .count(),

            "sending":

                EmailQueue.query
                .filter_by(
                    status="SENDING"
                )
                .count(),

            "sent":

                EmailQueue.query
                .filter_by(
                    status="SENT"
                )
                .count(),

            "retrying":

                EmailQueue.query
                .filter_by(
                    status="RETRYING"
                )
                .count(),

            "failed":

                EmailQueue.query
                .filter_by(
                    status="FAILED"
                )
                .count()

        }

    @staticmethod
    def failed_emails():

        return (

            EmailQueue.query

            .filter_by(
                status="FAILED"
            )

            .all()

        )

    @staticmethod
    def pending_emails():

        return (

            EmailQueue.query

            .filter(

                EmailQueue.status.in_(

                    [

                        "PENDING",

                        "RETRYING"

                    ]

                )

            )

            .all()

        )

    @staticmethod
    def mark_deleted(email_id):

        email = (
            EmailQueue.query.get(
                email_id
            )
        )

        if not email:
            return False

        email.deleted = True

        db.session.commit()

        return True