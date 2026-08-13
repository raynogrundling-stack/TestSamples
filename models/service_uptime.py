from datetime import datetime

from extensions import db


class ServiceUptime(db.Model):

    __tablename__ = "service_uptime"

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
        default="ONLINE"
    )

    uptime_seconds = db.Column(
        db.BigInteger,
        nullable=False,
        default=0
    )

    started_at = db.Column(
        db.DateTime,
        nullable=True
    )

    last_seen = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):

        return (
            f"<ServiceUptime "
            f"{self.service_name}>"
        )
