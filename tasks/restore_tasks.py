from datetime import datetime
from celery_worker import celery
from extensions import db
from models.restore_job import RestoreJob
from services.restore_service import (
    RestoreService
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
def run_restore_task(
    self,
    restore_job_id
):
    job = None
    try:
        job = RestoreJob.query.get(
            restore_job_id
        )
        if not job:
            raise Exception(
                f"Restore job "
                f"{restore_job_id} "
                f"not found."
            )
        job.status = "RUNNING"
        job.started_at = (
            datetime.utcnow()
        )
        job.progress_percent = 10
        job.current_step = (
            "Starting restore"
        )
        db.session.commit()
        logger.info(
            f"Starting restore "
            f"job {job.id}"
        )
        job.progress_percent = 50
        job.current_step = (
            "Restoring backup"
        )
        db.session.commit()
        RestoreService.restore_backup(
            job.backup_filename
        )
        job.progress_percent = 100
        job.current_step = (
            "Completed"
        )
        job.status = "COMPLETED"
        job.completed_at = (
            datetime.utcnow()
        )
        db.session.commit()
        AuditService.log(
            action="RESTORE_COMPLETED",
            object_type="RESTORE",
            object_id=str(job.id)
        )
        logger.info(
            f"Restore completed "
            f"for job {job.id}"
        )
        return True
    except Exception as ex:
        logger.exception(
            "Restore failed"
        )
        if job:
            job.status = "FAILED"
            job.error_message = str(ex)
            job.completed_at = (
                datetime.utcnow()
            )
            db.session.commit()
        try:
            FailureService.log_failure(
                source="restore_task",
                exception=ex
            )
        except Exception:
            pass
        raise
@celery.task(
    bind=True,
    max_retries=MAX_RETRIES
)
def rollback_restore(
    self,
    restore_job_id
):
    job = RestoreJob.query.get(
        restore_job_id
    )
    if not job:
        raise Exception(
            f"Restore job "
            f"{restore_job_id} "
            f"not found."
        )
    try:
        job.rollback_attempted = True
        db.session.commit()
        if not job.safety_backup_file:
            raise Exception(
                "No safety backup available."
            )
        RestoreService.restore_backup(
            job.safety_backup_file
        )
        job.rollback_successful = True
        job.rollback_completed_at = (
            datetime.utcnow()
        )
        db.session.commit()
        AuditService.log(
            action="RESTORE_ROLLBACK_COMPLETED",
            object_type="RESTORE",
            object_id=str(job.id)
        )
        return True
    except Exception as ex:
        job.rollback_successful = False
        job.rollback_error = str(ex)
        job.rollback_completed_at = (
            datetime.utcnow()
        )
        db.session.commit()
        logger.exception(
            "Rollback failed"
        )
        raise