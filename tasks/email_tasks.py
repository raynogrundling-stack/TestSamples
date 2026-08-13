from datetime import datetime

from celery_worker import celery

from extensions import db

from models.email_queue import EmailQueue
from models.submission import Submission

from services.email_queue_service import (
    EmailQueueService
)

from services.audit_service import (
    AuditService
)

from services.failure_service import (
    FailureService
)

from services.logger import logger


MAX_RETRIES = 5


@celery.task(
    bind=True,
    max_retries=MAX_RETRIES
)
def send_submission_email(
    self,
    submission_id
):
    """
    Creates an EmailQueue record
    for a submission email.
    """

    try:

        submission = (
            Submission.query.get(
                submission_id
            )
        )

        if not submission:

            raise Exception(
                f"Submission "
                f"{submission_id} "
                f"not found."
            )

        email_id = (

            EmailQueueService
            .queue_submission_email(
                submission
            )

        )

        AuditService.log(

            action="EMAIL_QUEUED",

            object_type="SUBMISSION",

            object_id=str(
                submission.id
            )

        )

        logger.info(

            f"Email queued "
            f"for submission "
            f"{submission.id}"

        )

        process_email_queue.delay(
            email_id
        )

        return True

    except Exception as ex:

        FailureService.log_failure(

            source=
            "Submission Email Queue",

            exception=ex,

            severity="ERROR"

        )

        logger.exception(
            "Unable to queue email"
        )

        raise self.retry(
            exc=ex,
            countdown=120
        )


@celery.task(
    bind=True,
    max_retries=MAX_RETRIES
)
def process_email_queue(
    self,
    email_id
):
    """
    Processes a single
    EmailQueue record.
    """

    email = None

    try:

        email = (
            EmailQueue.query.get(
                email_id
            )
        )

        if not email:

            raise Exception(
                f"Email queue item "
                f"{email_id} "
                f"not found."
            )

        email.status = "SENDING"

        email.processing_started_at = (
            datetime.utcnow()
        )

        db.session.commit()

        logger.info(

            f"Processing email "
            f"{email.id}"

        )

        send_start = (
            datetime.utcnow()
        )

        smtp_response = (

            EmailQueueService.send(
                email
            )

        )

        send_end = (
            datetime.utcnow()
        )

        email.processing_finished_at = (
            send_end
        )

        email.sent_at = send_end

        email.smtp_response = (
            smtp_response
        )

        email.delivery_duration_ms = int(

            (
                send_end - send_start
            ).total_seconds()

            * 1000

        )

        email.status = "SENT"

        email.failure_reason = None

        db.session.commit()

        AuditService.log(

            action="EMAIL_SENT",

            object_type="EMAIL",

            object_id=str(
                email.id
            )

        )

        logger.info(

            f"Email "
            f"{email.id} "
            f"sent successfully"

        )

        return True

    except Exception as ex:

        db.session.rollback()

        logger.exception(
            "Email send failed"
        )

        try:

            email = (
                EmailQueue.query.get(
                    email_id
                )
            )

            if email:

                email.retry_count = (
                    email.retry_count + 1
                )

                email.last_retry_at = (
                    datetime.utcnow()
                )

                email.failure_reason = (
                    str(ex)
                )

                if (
                    email.retry_count
                    >= MAX_RETRIES
                ):

                    email.status = "FAILED"

                else:

                    email.status = (
                        "RETRYING"
                    )

                db.session.commit()

        except Exception:

            db.session.rollback()

        FailureService.log_failure(

            source=
            "Email Queue Processor",

            exception=ex,

            severity="ERROR"

        )

        AuditService.log(

            action="EMAIL_FAILED",

            object_type="EMAIL",

            object_id=str(
                email_id
            ),

            details=str(ex)

        )

        raise self.retry(

            exc=ex,

            countdown=180

        )


@celery.task
def process_pending_emails():
    """
    Finds pending emails and
    queues each one for
    processing.
    """

    pending = (

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

    processed = 0

    for email in pending:

        process_email_queue.delay(
            email.id
        )

        processed += 1

    logger.info(

        f"Queued "
        f"{processed} "
        f"pending emails"

    )

    return processed


@celery.task
def cleanup_failed_emails():
    """
    Final cleanup task for
    emails exceeding retry
    limits.
    """

    emails = (

        EmailQueue.query

        .filter(

            EmailQueue.retry_count
            >= MAX_RETRIES

        )

        .filter(

            EmailQueue.status !=
            "FAILED"

        )

        .all()

    )

    count = 0

    for email in emails:

        email.status = "FAILED"

        count += 1

        AuditService.log(

            action=
            "EMAIL_PERMANENT_FAILURE",

            object_type="EMAIL",

            object_id=str(
                email.id
            )

        )

    db.session.commit()

    logger.warning(

        f"{count} emails marked "
        f"as permanently failed"

    )

    return count