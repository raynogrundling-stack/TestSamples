from datetime import datetime

from extensions import db


class FailureLog(db.Model):

    __tablename__ = "failure_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    source = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    severity = db.Column(
        db.String(50),
        nullable=False,
        default="ERROR",
        index=True
    )

    error_message = db.Column(
        db.Text,
        nullable=False
    )

    stack_trace = db.Column(
        db.Text,
        nullable=True
    )

    object_type = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    object_id = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=True,
        index=True
    )

    request_id = db.Column(
        db.String(255),
        nullable=True
    )

    resolved = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        index=True
    )

    resolution_notes = db.Column(
        db.Text,
        nullable=True
    )

    resolved_by = db.Column(
        db.Integer,
        nullable=True
    )

    resolved_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    def __repr__(self):

        return (
            f"<FailureLog "
            f"id={self.id}, "
            f"severity={self.severity}, "
            f"source={self.source}>"
        )

    @property
    def is_critical(self):

        return self.severity.upper() == "CRITICAL"

    @property
    def is_resolved(self):

        return self.resolved