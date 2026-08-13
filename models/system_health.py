from datetime import datetime

from extensions import db


class SystemHealth(db.Model):

    __tablename__ = "system_health"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    service_name = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="HEALTHY"
    )

    message = db.Column(
        db.Text,
        nullable=True
    )

    checked_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):

        return (
            f"<SystemHealth "
            f"{self.service_name}: "
            f"{self.status}>"
        )