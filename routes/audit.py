from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash
)
from flask_login import (
    login_required,
    current_user
)
from sqlalchemy import or_
from models.audit_log import (
    AuditLog
)
audit_bp = Blueprint(
    "audit",
    __name__,
    url_prefix="/admin/audit"
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
@audit_bp.route("/")
@login_required
@admin_required
def index():
    page = request.args.get(
        "page",
        1,
        type=int
    )
    search = request.args.get(
        "search",
        ""
    )
    query = AuditLog.query
    if search:
        query = query.filter(
            or_(
                AuditLog.action.ilike(
                    f"%{search}%"
                ),
                AuditLog.object_type.ilike(
                    f"%{search}%"
                ),
                AuditLog.object_id.ilike(
                    f"%{search}%"
                )
            )
        )
    pagination = (
        query
        .order_by(
            AuditLog.created_at.desc()
        )
        .paginate(
            page=page,
            per_page=50,
            error_out=False
        )
    )
    return render_template(
        "admin/audit/index.html",
        logs=pagination.items,
        pagination=pagination,
        search=search
    )
@audit_bp.route(
    "/<int:log_id>"
)
@login_required
@admin_required
def detail(log_id):
    log = AuditLog.query.get_or_404(
        log_id
    )
    return render_template(
        "admin/audit/detail.html",
        log=log
    )
@audit_bp.route(
    "/user/<int:user_id>"
)
@login_required
@admin_required
def user_activity(user_id):
    logs = (
        AuditLog.query
        .filter_by(
            user_id=user_id
        )
        .order_by(
            AuditLog.created_at.desc()
        )
        .all()
    )
    return render_template(
        "admin/audit/user_activity.html",
        logs=logs,
        user_id=user_id
    )
@audit_bp.route(
    "/api/recent"
)
@login_required
@admin_required
def api_recent():
    logs = (
        AuditLog.query
        .order_by(
            AuditLog.created_at.desc()
        )
        .limit(20)
        .all()
    )
    return jsonify([
        {
            "id":
            log.id,
            "action":
            log.action,
            "user_id":
            log.user_id,
            "object_type":
            log.object_type,
            "object_id":
            log.object_id,
            "created_at":
            str(log.created_at)
        }
        for log in logs
    ])