from functools import wraps

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

from sqlalchemy import or_

from extensions import db

from models.user import User

from forms.user_forms import (
    UserCreateForm,
    UserEditForm
)

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/admin/users"
)


def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not current_user.is_admin():

            flash(
                "Access denied.",
                "danger"
            )

            return redirect(
                url_for(
                    "main.index"
                )
            )

        return func(
            *args,
            **kwargs
        )

    return wrapper


@users_bp.route("/")
@login_required
@admin_required
def index():

    search = request.args.get(
        "search",
        ""
    )

    query = User.query

    if search:

        query = query.filter(
            or_(
                User.name.ilike(
                    f"%{search}%"
                ),

                User.surname.ilike(
                    f"%{search}%"
                ),

                User.contact_number.ilike(
                    f"%{search}%"
                ),

                User.email.ilike(
                    f"%{search}%"
                ),

                User.role.ilike(
                    f"%{search}%"
                )
            )
        )

    users = (
        query
        .order_by(
            User.name
        )
        .all()
    )

    return render_template(
        "admin/users/index.html",
        users=users,
        search=search
    )


@users_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def create():

    form = UserCreateForm()

    if form.validate_on_submit():

        existing = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing:

            flash(
                "Email address already exists.",
                "danger"
            )

            return render_template(
                "admin/users/create.html",
                form=form
            )

        user = User(

            name=form.name.data,

            surname=form.surname.data,

            contact_number=
                form.contact_number.data,

            email=form.email.data,

            role=form.role.data,

            active=form.active.data
        )

        if form.password.data:

            user.set_password(
                form.password.data
            )

        else:

            user.set_password(
                "Password123!"
            )

        db.session.add(
            user
        )

        db.session.commit()

        flash(
            "User created successfully.",
            "success"
        )

        return redirect(
            url_for(
                "users.index"
            )
        )

    return render_template(
        "admin/users/create.html",
        form=form
    )


@users_bp.route(
    "/<int:id>/edit",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit(id):

    user = User.query.get_or_404(
        id
    )

    form = UserEditForm(
        obj=user
    )

    if form.validate_on_submit():

        existing = User.query.filter(
            User.email == form.email.data,
            User.id != id
        ).first()

        if existing:

            flash(
                "Email address already exists.",
                "danger"
            )

            return render_template(
                "admin/users/edit.html",
                form=form,
                user=user
            )

        user.name = (
            form.name.data
        )

        user.surname = (
            form.surname.data
        )

        user.contact_number = (
            form.contact_number.data
        )

        user.email = (
            form.email.data
        )

        user.role = (
            form.role.data
        )

        user.active = (
            form.active.data
        )

        if form.password.data:

            user.set_password(
                form.password.data
            )

        db.session.commit()

        flash(
            "User updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "users.index"
            )
        )

    return render_template(
        "admin/users/edit.html",
        form=form,
        user=user
    )


@users_bp.route(
    "/<int:id>/toggle",
    methods=["POST"]
)
@login_required
@admin_required
def toggle(id):

    user = User.query.get_or_404(
        id
    )

    user.active = (
        not user.active
    )

    db.session.commit()

    flash(
        "User status updated.",
        "success"
    )

    return redirect(
        url_for(
            "users.index"
        )
    )


@users_bp.route(
    "/<int:id>/delete",
    methods=["POST"]
)
@login_required
@admin_required
def delete(id):

    user = User.query.get_or_404(
        id
    )

    if user.id == current_user.id:

        flash(
            "You cannot delete your own account.",
            "danger"
        )

        return redirect(
            url_for(
                "users.index"
            )
        )

    db.session.delete(
        user
    )

    db.session.commit()

    flash(
        "User deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "users.index"
        )
    )
