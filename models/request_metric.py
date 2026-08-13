from datetime import datetime

from extensions import db


class RequestMetric(db.Model):

    __tablename__ = "request_metrics"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    endpoint = db.Column(
        db.String(500),
        nullable=False,
        index=True
    )

    method = db.Column(
        db.String(20),
        nullable=False
    )

    status_code = db.Column(
        db.Integer,
        nullable=False
    )

    response_time_ms = db.Column(
        db.Float,
        nullable=True
    )

    ip_address = db.Column(
        db.String(100),
        nullable=True
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

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    def __repr__(self):

        return (
            f"<RequestMetric "
            f"{self.method} "
            f"{self.endpoint}>"
        )