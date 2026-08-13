from celery_worker import celery

from extensions import db

from models.submission import Submission

from services.pdf_service import (
    PDFService
)

from services.audit_service import (
    AuditService
)

from services.failure_service import (
    FailureService
)


@celery.task(
    bind=True,
    max_retries=3
)
def generate_pdf_task(
    self,
    submission_id
):

    try:

        submission = (
            Submission.query.get(
                submission_id
            )
        )

        if not submission:

            raise Exception(
                "Submission not found."
            )

        pdf_file = (

            PDFService.generate_pdf(
                submission
            )

        )

        submission.pdf_file = (
            pdf_file
        )

        submission.pdf_generated = True

        db.session.commit()

        AuditService.log(

            action=
            "PDF_GENERATED",

            object_type=
            "SUBMISSION",

            object_id=
            submission.id

        )

        return pdf_file

    except Exception as ex:

        db.session.rollback()

        FailureService.log_failure(

            source=
            "PDF Generation",

            exception=ex

        )

        raise self.retry(
            exc=ex,
            countdown=60
        )