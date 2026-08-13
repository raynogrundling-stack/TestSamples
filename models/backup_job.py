from datetime import datetime

from extensions import db


class BackupJob(db.Model):

    __tablename__ = "backup_jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    backup_filename = db.Column(
        db.String(500),
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="PENDING",
        index=True
    )

    progress_percent = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    current_step = db.Column(
        db.String(255),
        nullable=True
    )

    backup_type = db.Column(
        db.String(50),
        nullable=False,
        default="MANUAL"
    )

    file_size_bytes = db.Column(
        db.BigInteger,
        nullable=True
    )

    checksum = db.Column(
        db.String(255),
        nullable=True
    )

    verified = db.Column(
        db.Boolean,
        default=False
    )

    error_message = db.Column(
        db.Text,
        nullable=True
    )

    created_by = db.Column(
        db.Integer,
        nullable=True
    )

    started_at = db.Column(
        db.DateTime,
        nullable=True
    )

    completed_at = db.Column(
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
            f"<BackupJob "
            f"id={self.id}, "
            f"status={self.status}>"
        )

    @property
    def duration_seconds(self):

        if not self.started_at:
            return None

        if not self.completed_at:
            return None

        return int(

            (
                self.completed_at -
                self.started_at
            ).total_seconds()

        )