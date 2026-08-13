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
from models.restore_job import RestoreJob
from services.audit_service import AuditService
from tasks.restore_tasks import (
    run_restore_task,
    rollback_restore
)
restore_bp = Blueprint(
    "restore",
    __name__,
    url_prefix="/admin/restores"
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
@restore_bp.route("/")
@login_required
@admin_required
def index():
    page = request.args.get(
        "page",
        1,
        type=int
    )
    pagination = (
        RestoreJob.query
        .order_by(
            RestoreJob.id.desc()
        )
        .paginate(
            page=page,
            per_page=25,
            error_out=False
        )
    )
    return render_template(
        "admin/restores/index.html",
        restores=pagination.items,
        pagination=pagination
    )
@restore_bp.route(
    "/create",
    methods=["POST"]
)
@login_required
@admin_required
def create():
    backup_filename = request.form.get(
        "backup_filename"
    )
    if not backup_filename:
        flash(
            "Backup file required.",
            "danger"
        )
        return redirect(
            url_for("restore.index")
        )
    job = RestoreJob(
        backup_filename=backup_filename,
        started_by=current_user.id,
        status="PENDING"
    )
    db.session.add(job)
    db.session.commit()
    run_restore_task.delay(
        job.id
    )
    AuditService.log(
        action="RESTORE_CREATED",
        user_id=current_user.id,
        object_type="RESTORE",
        object_id=str(job.id)
    )
    flash(
        "Restore queued.",
        "success"
    )
    return redirect(
        url_for(
            "restore.details",
            restore_id=job.id
        )
    )
@restore_bp.route(
    "/<int:restore_id>"
)
@login_required
@admin_required
def details(restore_id):
    restore_job = (
        RestoreJob.query
        .get_or_404(restore_id)
    )
    return render_template(
        "admin/restores/details.html",
        restore_job=restore_job
    )
@restore_bp.route("/history")
@login_required
@admin_required
def history():
    restores = (
        RestoreJob.query
        .order_by(
            RestoreJob.created_at.desc()
        )
        .all()
    )
    return render_template(
        "admin/restores/history.html",
        restores=restores
    )
@restore_bp.route(
    "/rollback/<int:restore_id>",
    methods=["POST"]
)
@login_required
@admin_required
def rollback(restore_id):
    restore_job = (
        RestoreJob.query
        .get_or_404(restore_id)
    )
    rollback_restore.delay(
        restore_job.id
    )
    AuditService.log(
        action="RESTORE_ROLLBACK_REQUESTED",
        user_id=current_user.id,
        object_type="RESTORE",
        object_id=str(restore_job.id)
    )
    flash(
        "Rollback queued.",
        "warning"
    )
    return redirect(
        url_for(
            "restore.details",
            restore_id=restore_job.id
        )
    )
@restore_bp.route(
    "/status/<int:restore_id>"
)
@login_required
@admin_required
def status(restore_id):
    restore_job = (
        RestoreJob.query
        .get_or_404(restore_id)
    )
    return jsonify({
        "id": restore_job.id,
        "status": restore_job.status,
        "progress": restore_job.progress_percent,
        "current_step": restore_job.current_step,
        "started_at": (
            str(restore_job.started_at)
            if restore_job.started_at
            else None
        ),
        "completed_at": (
            str(restore_job.completed_at)
            if restore_job.completed_at
            else None
        )
    })
@restore_bp.route(
    "/delete/<int:restore_id>",
    methods=["POST"]
)
@login_required
@admin_required
def delete(restore_id):
    restore_job = (
        RestoreJob.query
        .get_or_404(restore_id)
    )
    db.session.delete(
        restore_job
    )
    db.session.commit()
    AuditService.log(
        action="RESTORE_DELETED",
        user_id=current_user.id,
        object_type="RESTORE",
        object_id=str(restore_job.id)
    )
    flash(
        "Restore job deleted.",
        "success"
    )
    return redirect(
        url_for("restore.index")
    )