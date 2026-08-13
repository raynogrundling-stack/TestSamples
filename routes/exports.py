from flask import (
    Blueprint,
    render_template,
    send_file,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from services.export_service import (
    ExportService
)

from services.audit_service import (
    AuditService
)


exports_bp = Blueprint(
    "exports",
    __name__,
    url_prefix="/admin/export"
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

            return redirect(
                url_for("main.index")
            )

        return func(
            *args,
            **kwargs
        )

    return wrapper


@exports_bp.route("/")
@login_required
@admin_required
def index():

    return render_template(
        "admin/export/index.html"
    )


# -------------------------
# Customers
# -------------------------

@exports_bp.route("/customers")
@login_required
@admin_required
def customers():

    return render_template(
        "admin/export/customers.html"
    )


@exports_bp.route("/customers/download")
@login_required
@admin_required
def customers_download():

    export_file = (
        ExportService.export_customers_csv()
    )

    AuditService.log(
        action="CUSTOMERS_EXPORTED",
        user_id=current_user.id,
        object_type="EXPORT"
    )

    return send_file(
        export_file,
        as_attachment=True
    )


# -------------------------
# Users
# -------------------------

@exports_bp.route("/users")
@login_required
@admin_required
def users():

    return render_template(
        "admin/export/users.html"
    )


@exports_bp.route("/users/download")
@login_required
@admin_required
def users_download():

    export_file = (
        ExportService.export_users_csv()
    )

    AuditService.log(
        action="USERS_EXPORTED",
        user_id=current_user.id,
        object_type="EXPORT"
    )

    return send_file(
        export_file,
        as_attachment=True
    )


# -------------------------
# Dropdowns
# -------------------------

@exports_bp.route("/dropdowns")
@login_required
@admin_required
def dropdowns():

    return render_template(
        "admin/export/dropdowns.html"
    )


@exports_bp.route("/dropdowns/download")
@login_required
@admin_required
def dropdowns_download():

    export_file = (
        ExportService.export_dropdowns_csv()
    )

    AuditService.log(
        action="DROPDOWNS_EXPORTED",
        user_id=current_user.id,
        object_type="EXPORT"
    )

    return send_file(
        export_file,
        as_attachment=True
    )


# -------------------------
# Audit Logs
# -------------------------

@exports_bp.route("/audit")
@login_required
@admin_required
def audit_logs():

    return render_template(
        "admin/export/audit.html"
    )


@exports_bp.route("/audit/download")
@login_required
@admin_required
def audit_download():

    export_file = (
        ExportService.export_audit_csv()
    )

    AuditService.log(
        action="AUDIT_EXPORTED",
        user_id=current_user.id,
        object_type="EXPORT"
    )

    return send_file(
        export_file,
        as_attachment=True
    )


# -------------------------
# System Export
# -------------------------

@exports_bp.route("/system")
@login_required
@admin_required
def system_export():

    return render_template(
        "admin/export/system.html"
    )


@exports_bp.route("/system/download")
@login_required
@admin_required
def system_download():

    export_file = (
        ExportService.export_complete_system_zip()
    )

    AuditService.log(
        action="SYSTEM_EXPORTED",
        user_id=current_user.id,
        object_type="EXPORT"
    )

    return send_file(
        export_file,
        as_attachment=True
    )