from extensions import db

from models.audit_log import (
    AuditLog
)


class AuditService:

    @staticmethod
    def log(

        action,

        user_id=None,

        object_type=None,

        object_id=None,

        details=None

    ):

        entry = AuditLog(

            action=action,

            user_id=user_id,

            object_type=object_type,

            object_id=object_id,

            details=details

        )

        db.session.add(entry)

        db.session.commit()