from flask import (
    Blueprint,
    render_template,
    jsonify,
    redirect,
    flash
)
from flask_login import (
    login_required,
    current_user
)
from services.audit_service import (
    AuditService
)
migrations_bp = Blueprint(
    "migrations",
    __name__,
    url_prefix="/admin/migrations"
)
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect("/auth/login")
        if not current_user.is_admin():
            flash(
                "Administrator access required.",
                "danger"
            )
            return redirect("/")
        return func(
            *args,
            **kwargs
        )
    return wrapper
@migrations_bp.route("/")
@login_required
@admin_required
def index():
    return render_template(
        "admin/migrations/index.html"
    )
@migrations_bp.route("/current")
@login_required
@admin_required
def current():
    return render_template(
        "admin/migrations/current.html"
    )
@migrations_bp.route("/history")
@login_required
@admin_required
def history():
    return render_template(
        "admin/migrations/history.html"
    )
@migrations_bp.route("/failures")
@login_required
@admin_required
def failures():
    return render_template(
        "admin/migrations/failures.html"
    )
@migrations_bp.route("/api/status")
@login_required
@admin_required
def api_status():
    return jsonify({
        "status": "available",
        "migration_system":
        "Flask-Migrate/Alembic"
    })
@migrations_bp.route("/refresh")
@login_required
@admin_required
def refresh():
    AuditService.log(
        action=
        "MIGRATION_STATUS_REFRESHED",
        user_id=
        current_user.id,
        object_type=
        "MIGRATION"
    )
    flash(
        "Migration status refreshed.",
        "success"
    )
    return redirect(
        "/admin/migrations"
    )