from datetime import datetime

from celery_worker import celery

from extensions import db

from models.backup_job import BackupJob

from services.backup_service import (
    BackupService
)

from services.audit_service import (
    AuditService
)

from services.failure_service import (
    FailureService
)

from services.logger import logger


MAX_RETRIES = 3


@celery.task(
    bind=True,
    max_retries=MAX_RETRIES
)
def run_backup_task(
    self,
    backup_job_id
):
    """
    Executes a single backup job.
    """

    job = None

    try:

        job = BackupJob.query.get(
            backup_job_id
        )

        if not job:

            raise Exception(
                f"Backup job "
                f"{backup_job_id} "
                f"not found."
            )

        job.status = "RUNNING"

        job.started_at = (
            datetime.utcnow()
        )

        job.progress_percent = 5

        job.current_step = (
            "Initializing"
        )

        db.session.commit()

        logger.info(
            f"Starting backup "
            f"job {job.id}"
        )

        #
        # Create backup
        #

        job.progress_percent = 25

        job.current_step = (
            "Creating backup"
        )

        db.session.commit()

        backup_file = (
            BackupService.create_backup(
                job.id
            )
        )

        #
        # Verify backup
        #

        job.progress_percent = 80

        job.current_step = (
            "Verifying backup"
        )

        db.session.commit()

        valid = (
            BackupService.verify_backup(
                backup_file
            )
        )

        if not valid:

            raise Exception(
                "Backup validation failed."
            )

        #
        # Complete
        #

        job.progress_percent = 100

        job.current_step = (
            "Completed"
        )

        job.status = "COMPLETED"

        job.backup_filename = (
            backup_file
        )

        job.completed_at = (
            datetime.utcnow()
        )

        db.session.commit()

        AuditService.log(

            action=
            "BACKUP_COMPLETED",

            object_type=
            "BACKUP",

            object_id=str(
                job.id
            )

        )

        logger.info(

            f"Backup "
            f"{job.id} complete"

        )

        return backup_file

    except Exception as ex:

        db.session.rollback()

        logger.exception(
            "Backup failed"
        )

        try:

            job = (
                BackupJob.query.get(
                    backup_job_id
                )
            )

            if job:

                job.status = "FAILED"

                job.error_message = (
                    str(ex)
                )

                job.completed_at = (
                    datetime.utcnow()
                )

                db.session.commit()

        except Exception:

            db.session.rollback()

        FailureService.log_failure(

            source=
            "Backup Task",

            exception=ex,

            severity="CRITICAL"

        )

        AuditService.log(

            action=
            "BACKUP_FAILED",

            object_type=
            "BACKUP",

            object_id=str(
                backup_job_id
            ),

            details=str(ex)

        )

        raise self.retry(
            exc=ex,
            countdown=300
        )


@celery.task
def scheduled_backup():
    """
    Creates and starts
    a scheduled backup.
    """

    try:

        logger.info(
            "Starting scheduled backup"
        )

        job = (
            BackupService
            .create_backup_job()
        )

        run_backup_task.delay(
            job.id
        )

        return job.id

    except Exception as ex:

        logger.exception(
            "Scheduled backup failed"
        )

        FailureService.log_failure(

            source=
            "Scheduled Backup",

            exception=ex,

            severity="CRITICAL"

        )

        return None


@celery.task
def cleanup_old_backups(
    keep_days=30
):
    """
    Removes backup files older
    than keep_days.
    """

    try:

        removed = (
            BackupService
            .cleanup_backups(
                keep_days
            )
        )

        AuditService.log(

            action=
            "BACKUP_CLEANUP",

            details=
            f"Removed "
            f"{removed} backup(s)"

        )

        logger.info(

            f"Removed "
            f"{removed} backups"

        )

        return removed

    except Exception as ex:

        logger.exception(
            "Backup cleanup failed"
        )

        FailureService.log_failure(

            source=
            "Backup Cleanup",

            exception=ex

        )

        return 0


@celery.task
def verify_all_backups():
    """
    Verifies all backup files.
    """

    try:

        results = (
            BackupService
            .verify_all_backups()
        )

        AuditService.log(

            action=
            "BACKUP_VERIFICATION"

        )

        return results

    except Exception as ex:

        logger.exception(
            "Backup verification failed"
        )

        FailureService.log_failure(

            source=
            "Backup Verification",

            exception=ex

        )

        return {
            "success": False
        }