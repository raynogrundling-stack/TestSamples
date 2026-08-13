from datetime import datetime

from extensions import db


class RestoreJob(db.Model):

    __tablename__ = "restore_jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    backup_filename = db.Column(
        db.String(500),
        nullable=False
    )

    safety_backup_file = db.Column(
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

    error_message = db.Column(
        db.Text,
        nullable=True
    )

    started_by = db.Column(
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

    rollback_attempted = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    rollback_successful = db.Column(
        db.Boolean,
        nullable=True
    )

    rollback_error = db.Column(
        db.Text,
        nullable=True
    )

    rollback_completed_at = db.Column(
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
            f"<RestoreJob "
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

    @property
    def rollback_duration_seconds(self):

        if not self.rollback_attempted:
            return None

        if not self.rollback_completed_at:
            return None

        if not self.completed_at:
            return None

        return int(
            (
                self.rollback_completed_at -
                self.completed_at
            ).total_seconds()
        )