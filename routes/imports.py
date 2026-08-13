from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from services.import_service import (
    ImportService
)

from services.audit_service import (
    AuditService
)


imports_bp = Blueprint(
    "imports",
    __name__,
    url_prefix="/admin/imports"
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


@imports_bp.route("/")
@login_required
@admin_required
def index():

    return render_template(
        "admin/import/index.html"
    )


@imports_bp.route(
    "/customers",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def customers():

    if request.method == "POST":

        upload = request.files.get(
            "file"
        )

        if not upload:

            flash(
                "Please select a file.",
                "danger"
            )

            return redirect(
                url_for(
                    "imports.customers"
                )
            )

        result = (
            ImportService
            .import_customers(
                upload
            )
        )

        AuditService.log(

            action=
            "CUSTOMERS_IMPORTED",

            user_id=
            current_user.id,

            object_type=
            "IMPORT",

            details=str(result)

        )

        flash(
            "Customer import completed.",
            "success"
        )

        return redirect(
            url_for(
                "imports.index"
            )
        )

    return render_template(
        "admin/import/customers.html"
    )


@imports_bp.route(
    "/dropdowns",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def dropdowns():

    if request.method == "POST":

        upload = request.files.get(
            "file"
        )

        if not upload:

            flash(
                "Please select a file.",
                "danger"
            )

            return redirect(
                url_for(
                    "imports.dropdowns"
                )
            )

        result = (
            ImportService
            .import_dropdowns(
                upload
            )
        )

        AuditService.log(

            action=
            "DROPDOWNS_IMPORTED",

            user_id=
            current_user.id,

            object_type=
            "IMPORT",

            details=str(result)

        )

        flash(
            "Dropdown import completed.",
            "success"
        )

        return redirect(
            url_for(
                "imports.index"
            )
        )

    return render_template(
        "admin/import/dropdowns.html"
    )


@imports_bp.route(
    "/settings",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def settings():

    if request.method == "POST":

        upload = request.files.get(
            "file"
        )

        if not upload:

            flash(
                "Please select a file.",
                "danger"
            )

            return redirect(
                url_for(
                    "imports.settings"
                )
            )

        result = (
            ImportService
            .import_settings(
                upload
            )
        )

        AuditService.log(

            action=
            "SETTINGS_IMPORTED",

            user_id=
            current_user.id,

            object_type=
            "IMPORT",

            details=str(result)

        )

        flash(
            "Settings import completed.",
            "success"
        )

        return redirect(
            url_for(
                "imports.index"
            )
        )

    return render_template(
        "admin/import/settings.html"
    )


@imports_bp.route(
    "/backup",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def backup_zip():

    if request.method == "POST":

        upload = request.files.get(
            "file"
        )

        if not upload:

            flash(
                "Please select a backup file.",
                "danger"
            )

            return redirect(
                url_for(
                    "imports.backup_zip"
                )
            )

        result = (
            ImportService
            .import_backup_zip(
                upload
            )
        )

        AuditService.log(

            action=
            "BACKUP_IMPORTED",

            user_id=
            current_user.id,

            object_type=
            "IMPORT",

            details=str(result)

        )

        flash(
            "Backup imported successfully.",
            "success"
        )

        return redirect(
            url_for(
                "imports.index"
            )
        )

    return render_template(
        "admin/import/backup_zip.html"
    )