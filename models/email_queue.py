from datetime import datetime

from extensions import db


class EmailQueue(db.Model):

    __tablename__ = "email_queue"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    submission_id = db.Column(
        db.Integer,
        nullable=True
    )

    recipients = db.Column(
        db.JSON,
        nullable=False
    )

    subject = db.Column(
        db.String(500),
        nullable=False
    )

    body = db.Column(
        db.Text,
        nullable=False
    )

    attachments = db.Column(
        db.JSON,
        default=list
    )

    email_type = db.Column(
        db.String(50),
        default="GENERAL"
    )

    status = db.Column(
        db.String(50),
        default="PENDING"
    )

    retry_count = db.Column(
        db.Integer,
        default=0
    )

    recipient_count = db.Column(
        db.Integer,
        default=0
    )

    attachment_count = db.Column(
        db.Integer,
        default=0
    )

    smtp_response = db.Column(
        db.Text
    )

    failure_reason = db.Column(
        db.Text
    )

    processing_started_at = db.Column(
        db.DateTime
    )

    processing_finished_at = db.Column(
        db.DateTime
    )

    sent_at = db.Column(
        db.DateTime
    )

    last_retry_at = db.Column(
        db.DateTime
    )

    delivery_duration_ms = db.Column(
        db.Integer
    )

    deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    deleted_at = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )