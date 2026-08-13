from extensions import db

from models.failure_log import (
    FailureLog
)


class FailureService:

    @staticmethod
    def log_failure(

        source,

        exception,

        severity="ERROR"

    ):

        failure = FailureLog(

            source=source,

            severity=severity,

            error_message=str(exception)

        )

        db.session.add(
            failure
        )

        db.session.commit()