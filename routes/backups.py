from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify
)
from flask_login import (
    login_required,
    current_user
)
from extensions import db
from models.backup_job import BackupJob
from services.audit_service import AuditService
from tasks.backup_tasks import (
    run_backup_task,
    scheduled_backup,
    cleanup_old_backups
)
backups_bp = Blueprint(
    "backups",
    __name__,
    url_prefix="/admin/backups"
)
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            flash(
                "Access denied.",
                "danger"
            )
            return redirect("/")
        return func(
            *args,
            **kwargs
        )
    return wrapper
@backups_bp.route("/")
@login_required
@admin_required
def index():
    page = request.args.get(
        "page",
        1,
        type=int
    )
    pagination = (
        BackupJob.query
        .order_by(
            BackupJob.id.desc()
        )
        .paginate(
            page=page,
            per_page=25,
            error_out=False
        )
    )
    return render_template(
        "admin/backups/index.html",
        backups=pagination.items,
        pagination=pagination
    )
@backups_bp.route(
    "/create",
    methods=["POST"]
)
@login_required
@admin_required
def create():
    job = BackupJob(
        status="PENDING",
        backup_type="MANUAL",
        created_by=current_user.id
    )
    db.session.add(job)
    db.session.commit()
    run_backup_task.delay(job.id)
    AuditService.log(
        action="BACKUP_CREATED",
        user_id=current_user.id,
        object_type="BACKUP",
        object_id=str(job.id)
    )
    flash(
        "Backup queued.",
        "success"
    )
    return redirect(
        url_for(
            "backups.details",
            backup_id=job.id
        )
    )
@backups_bp.route(
    "/<int:backup_id>"
)
@login_required
@admin_required
def details(backup_id):
    backup_job = BackupJob.query.get_or_404(
        backup_id
    )
    return render_template(
        "admin/backups/details.html",
        backup_job=backup_job
    )
@backups_bp.route("/history")
@login_required
@admin_required
def history():
    backups = (
        BackupJob.query
        .order_by(
            BackupJob.created_at.desc()
        )
        .all()
    )
    return render_template(
        "admin/backups/history.html",
        backups=backups
    )
@backups_bp.route(
    "/cleanup",
    methods=["POST"]
)
@login_required
@admin_required
def cleanup():
    keep_days = request.form.get(
        "keep_days",
        30,
        type=int
    )
    cleanup_old_backups.delay(
        keep_days
    )
    AuditService.log(
        action="BACKUP_CLEANUP_REQUESTED",
        user_id=current_user.id,
        details=f"Retention={keep_days}"
    )
    flash(
        "Backup cleanup queued.",
        "success"
    )
    return redirect(
        url_for("backups.index")
    )
@backups_bp.route(
    "/scheduled",
    methods=["POST"]
)
@login_required
@admin_required
def run_scheduled():
    scheduled_backup.delay()
    AuditService.log(
        action="SCHEDULED_BACKUP_STARTED",
        user_id=current_user.id
    )
    flash(
        "Scheduled backup queued.",
        "success"
    )
    return redirect(
        url_for("backups.index")
    )
@backups_bp.route(
    "/status/<int:backup_id>"
)
@login_required
@admin_required
def status(backup_id):
    backup_job = BackupJob.query.get_or_404(
        backup_id
    )
    return jsonify({
        "id": backup_job.id,
        "status": backup_job.status,
        "progress": backup_job.progress_percent,
        "current_step": backup_job.current_step,
        "filename": backup_job.backup_filename,
        "started_at": (
            str(backup_job.started_at)
            if backup_job.started_at
            else None
        ),
        "completed_at": (
            str(backup_job.completed_at)
            if backup_job.completed_at
            else None
        )
    })
@backups_bp.route(
    "/delete/<int:backup_id>",
    methods=["POST"]
)
@login_required
@admin_required
def delete(backup_id):
    backup_job = BackupJob.query.get_or_404(
        backup_id
    )
    db.session.delete(
        backup_job
    )
    db.session.commit()
    AuditService.log(
        action="BACKUP_DELETED",
        user_id=current_user.id,
        object_type="BACKUP",
        object_id=str(backup_job.id)
    )
    flash(
        "Backup job deleted.",
        "success"
    )
    return redirect(
        url_for("backups.index")
    )