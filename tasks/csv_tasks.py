from celery_worker import celery

from extensions import db

from models.submission import Submission

from services.csv_service import (
    CSVService
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
def generate_csv_task(
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

        csv_file = (

            CSVService.generate_csv(
                submission
            )

        )

        submission.csv_file = (
            csv_file
        )

        submission.csv_generated = True

        db.session.commit()

        AuditService.log(

            action=
            "CSV_GENERATED",

            object_type=
            "SUBMISSION",

            object_id=
            submission.id

        )

        return csv_file

    except Exception as ex:

        db.session.rollback()

        FailureService.log_failure(

            source=
            "CSV Generation",

            exception=ex

        )

        raise self.retry(
            exc=ex,
            countdown=60
        )