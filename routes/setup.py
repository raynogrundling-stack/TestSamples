from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify
)
from extensions import db
from models.system_settings import (
    SystemSettings
)
from models.user import (
    User
)
from forms.settings_forms import (
    SetupWizardForm
)
from services.audit_service import (
    AuditService
)
setup_bp = Blueprint(
    "setup",
    __name__,
    url_prefix="/setup"
)
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
@setup_bp.route(
    "/",
    methods=["GET", "POST"]
)
def index():
    settings = get_settings()
    #
    # Prevent setup reruns
    #
    if settings.setup_completed:
        flash(
            "System setup has already been completed.",
            "warning"
        )
        return redirect(
            url_for(
                "auth.login"
            )
        )
    form = SetupWizardForm(
        obj=settings
    )
    if form.validate_on_submit():
        #
        # Sandbox
        #
        settings.sandbox_enabled = (
            form.sandbox_enabled.data
        )
        if (
            settings.sandbox_enabled
            and
            not settings.sandbox_initialized_at
        ):
            settings.sandbox_initialized_at = (
                datetime.utcnow()
            )
        #
        # Company
        #
        settings.company_name = (
            form.company_name.data
        )
        #
        # SMTP
        #
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
        #
        # Create First Admin
        #
        if User.query.count() == 0:
            admin = User(
                name=form.admin_name.data,
                email=form.admin_email.data,
                role="admin",
                active=True
            )
            print(
                "SETUP PASSWORD:",
                repr(
                    form.admin_password.data
                )
            )
            admin.set_password(
                form.admin_password.data
            )
            db.session.add(
                admin
            )
        #
        # Complete setup
        #
        settings.setup_completed = True
        db.session.commit()
        try:
            AuditService.log(
                action=
                "SYSTEM_SETUP_COMPLETED",
                user_id=None,
                object_type=
                "SYSTEM"
            )
        except Exception:
            pass
        flash(
            "Setup completed successfully.",
            "success"
        )
        return redirect(
            url_for(
                "auth.login"
            )
        )
    return render_template(
        "admin/setup/index.html",
        form=form,
        settings=settings
    )
@setup_bp.route("/status")
def status():
    settings = (
        SystemSettings.query.first()
    )
    if not settings:
        return jsonify({
            "configured": False
        })
    return jsonify({
        "configured":
        settings.setup_completed,
        "sandbox_enabled":
        settings.sandbox_enabled,
        "company_name":
        settings.company_name
    })
@setup_bp.route(
    "/reset",
    methods=["POST"]
)
def reset():
    settings = (
        SystemSettings.query.first()
    )
    if not settings:
        return redirect(
            url_for(
                "setup.index"
            )
        )
    settings.setup_completed = False
    db.session.commit()
    flash(
        "Setup reset.",
        "warning"
    )
    return redirect(
        url_for(
            "setup.index"
        )
    )