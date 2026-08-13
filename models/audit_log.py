from datetime import datetime

from extensions import db


class AuditLog(db.Model):

    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    action = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=True,
        index=True
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

    details = db.Column(
        db.Text,
        nullable=True
    )

    ip_address = db.Column(
        db.String(100),
        nullable=True
    )

    request_id = db.Column(
        db.String(255),
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
            f"<AuditLog "
            f"{self.action}>"
        )