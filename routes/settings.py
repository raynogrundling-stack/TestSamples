from pathlib import Path
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app
)
from flask_login import (
    login_required,
    current_user
)
from werkzeug.utils import (
secure_filename
)
from extensions import db
from models.system_settings import (
    SystemSettings
)
from forms.settings_forms import (
    CompanySettingsForm,
    SMTPSettingsForm,
    SecuritySettingsForm,
    MonitoringSettingsForm,
    PrintingSettingsForm
)
from services.audit_service import (
    AuditService
)
from services.smtp_test_service import (
    SMTPTestService
)
from services.sandbox_service import (
    SandboxService
)
settings_bp = Blueprint(
    "settings",
    __name__,
    url_prefix="/admin/settings"
)
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(
                url_for("auth.login")
            )
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
def get_settings():
    settings = (
        SystemSettings.query.first()
    )
    if not settings:
        settings = SystemSettings()
        db.session.add(
            settings
        )
        db.session.commit()
    return settings
@settings_bp.route("/")
@login_required
@admin_required
def index():
    settings = get_settings()
    return render_template(
        "admin/settings/index.html",
        settings=settings
    )
@settings_bp.route(
    "/company",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def company():
    settings = get_settings()
    form = CompanySettingsForm(
        obj=settings
    )
    if form.validate_on_submit():
    settings.company_name = (
        form.company_name.data
    )

    settings.submission_email = (
        form.submission_email.data
    )
        logo = request.files.get(
            "company_logo"
        )
        #
        # Remove existing logo
        #
        if (
            form.remove_logo.data
            and
            settings.company_logo
        ):
            logo_path = (
                Path(current_app.root_path)
                / "static"
                / "uploads"
                / "logos"
                / "company_logo.png"
            )
            if logo_path.exists():
                logo_path.unlink()

            settings.company_logo = None
        #
        # Upload new logo
        #
        elif (
            logo
            and
            logo.filename
        ):
            upload_folder = (
                Path(current_app.root_path)
                / "static"
                / "uploads"
                / "logos"
            )
            upload_folder.mkdir(
                parents=True,
                exist_ok=True
            )
            filename = (
                "company_logo.png"
            )
            logo.save(
                upload_folder / filename
            )
            settings.company_logo = (
                "uploads/logos/company_logo.png"
            )
        db.session.commit()
        AuditService.log(
            action="SETTINGS_COMPANY_UPDATED",
            user_id=current_user.id
        )
        flash(
            "Company settings saved.",
            "success"
        )
        return redirect(
            url_for(
                "settings.company"
            )
        )
    return render_template(
        "admin/settings/company.html",
        form=form,
        settings=settings
    )
@settings_bp.route(
    "/smtp",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def smtp():
    settings = get_settings()
    form = SMTPSettingsForm(
        obj=settings
    )
    if form.validate_on_submit():
        settings.smtp_server = (
            form.smtp_server.data
        )
        settings.smtp_port = (
            form.smtp_port.data
        )
        settings.smtp_username = (
            form.smtp_username.data
        )
        settings.smtp_password = (
            form.smtp_password.data
        )
        settings.smtp_sender_name = (
            form.smtp_sender_name.data
        )
        settings.smtp_sender_address = (
            form.smtp_sender_address.data
        )
        settings.smtp_use_tls = (
            form.smtp_use_tls.data
        )
        db.session.commit()
        AuditService.log(
            action="SETTINGS_SMTP_UPDATED",
            user_id=current_user.id
        )
        flash(
            "SMTP settings saved.",
            "success"
        )
        return redirect(
            url_for(
                "settings.smtp"
            )
        )
    return render_template(
        "admin/settings/smtp.html",
        form=form
    )
@settings_bp.route(
    "/smtp/test",
    methods=["POST"]
)
@login_required
@admin_required
def smtp_test():
    try:
        SMTPTestService.send_test_email()
        flash(
            "SMTP test successful.",
            "success"
        )
    except Exception as ex:
        flash(
            str(ex),
            "danger"
        )
    return redirect(
        url_for(
            "settings.smtp"
        )
    )
@settings_bp.route(
    "/security",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def security():
    settings = get_settings()
    form = SecuritySettingsForm(
        obj=settings
    )
    if form.validate_on_submit():
        settings.max_login_attempts = (
            form.max_login_attempts.data
        )
        settings.session_timeout_minutes = (
            form.session_timeout_minutes.data
        )
        db.session.commit()
        AuditService.log(
            action="SETTINGS_SECURITY_UPDATED",
            user_id=current_user.id
        )
        flash(
            "Security settings saved.",
            "success"
        )
        return redirect(
            url_for(
                "settings.security"
            )
        )
    return render_template(
        "admin/settings/security.html",
        form=form
    )
@settings_bp.route(
    "/monitoring",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def monitoring():
    settings = get_settings()
    form = MonitoringSettingsForm(
        obj=settings
    )
    if form.validate_on_submit():
        old_sandbox_value = (
            settings.sandbox_enabled
        )
        settings.monitoring_enabled = (
            form.monitoring_enabled.data
        )
        settings.prometheus_enabled = (
            form.prometheus_enabled.data
        )
        settings.grafana_enabled = (
            form.grafana_enabled.data
        )
        settings.sandbox_enabled = (
            form.sandbox_enabled.data
        )
        db.session.commit()
        AuditService.log(
            action="SETTINGS_MONITORING_UPDATED",
            user_id=current_user.id
        )
        if (
            old_sandbox_value
            and
            not settings.sandbox_enabled
        ):
            return redirect(
                url_for(
                    "settings.disable_sandbox"
                )
            )
        flash(
            "Monitoring settings saved.",
            "success"
        )
        return redirect(
            url_for(
                "settings.monitoring"
            )
        )
    return render_template(
        "admin/settings/monitoring.html",
        form=form
    )
@settings_bp.route(
    "/printing",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def printing():
    settings = get_settings()
    form = PrintingSettingsForm(
        obj=settings
    )
    if form.validate_on_submit():
        settings.auto_print_on_submit = (
            form.auto_print_on_submit.data
        )
        settings.enable_browser_printing = (
            form.enable_browser_printing.data
        )
        db.session.commit()
        AuditService.log(
            action="SETTINGS_PRINTING_UPDATED",
            user_id=current_user.id
        )
        flash(
            "Printing settings saved.",
            "success"
        )
        return redirect(
            url_for(
                "settings.printing"
            )
        )
    return render_template(
        "admin/settings/printing.html",
        form=form
    )
@settings_bp.route(
    "/sandbox/disable",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def disable_sandbox():
    SandboxService.disable_sandbox()
    flash(
        (
            "Sandbox disabled. "
            "Please complete production setup."
        ),
        "warning"
    )
    return redirect(
        url_for(
            "setup.index"
        )
    )
