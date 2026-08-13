from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from extensions import db
from models.user import User
from forms.auth_forms import (
    LoginForm,
    RegisterForm,
    RequestResetForm,
    ResetPasswordForm
)
from services.email_service import (
    EmailService
)
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)
@auth_bp.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def request_reset():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data
        ).first()
        if user:
            EmailService.send_reset_email(
                user
            )
        flash(
            "If the email exists, a reset link has been sent.",
            "info"
        )
        return redirect(
            url_for("auth.login")
        )
    return render_template(
        "auth/forgot_password.html",
        form=form
    )
@auth_bp.route(
    "/reset-password/<token>",
    methods=["GET", "POST"]
)
def reset_password(token):
    user = User.verify_reset_token(
        token
    )
    if not user:
        flash(
            "Invalid or expired token.",
            "danger"
        )
        return redirect(
            url_for(
                "auth.request_reset"
            )
        )
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = (
            generate_password_hash(
                form.password.data
            )
        )
        db.session.commit()
        flash(
            "Password updated successfully.",
            "success"
        )
        return redirect(
            url_for("auth.login")
        )
    return render_template(
        "auth/reset_password.html",
        form=form
    )
@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(
                url_for(
                    "settings.index"
                )
            )
        return redirect(
            url_for(
                "submissions.dashboard"
            )
        )
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data
        ).first()
        if (
            user
            and
            check_password_hash(
                user.password_hash,
                form.password.data
            )
        ):
            if not user.active:
                flash(
                    "Account disabled.",
                    "danger"
                )
                return redirect(
                    url_for(
                        "auth.login"
                    )
                )
            login_user(user)
            flash(
                "Logged in successfully.",
                "success"
            )
            if user.is_admin():
                return redirect(
                    url_for(
                        "settings.index"
                    )
                )
            return redirect(
                url_for(
                    "submissions.dashboard"
                )
            )
        flash(
            "Invalid email or password.",
            "danger"
        )
    return render_template(
        "auth/login.html",
        form=form
    )
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash(
        "You have been logged out.",
        "info"
    )
    return redirect(
        url_for("auth.login")
    )
@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(
            email=form.email.data
        ).first()
        if existing:
            flash(
                "Email already registered.",
                "warning"
            )
            return render_template(
                "auth/register.html",
                form=form
            )
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=
            generate_password_hash(
                form.password.data
            ),
            role="user",
            active=True
        )
        db.session.add(user)
        db.session.commit()
        flash(
            "Registration successful.",
            "success"
        )
        return redirect(
            url_for("auth.login")
        )
    return render_template(
        "auth/register.html",
        form=form
    )