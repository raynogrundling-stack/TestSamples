from datetime import datetime

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

from extensions import db

from models.dropdown_category import (
    DropdownCategory
)

from models.dropdown_option import (
    DropdownOption
)

dropdowns_bp = Blueprint(
    "dropdowns",
    __name__,
    url_prefix="/admin/dropdowns"
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
                url_for(
                    "auth.login"
                )
            )

        return func(
            *args,
            **kwargs
        )

    return wrapper


@dropdowns_bp.route("/")
@login_required
@admin_required
def index():

    categories = (
        DropdownCategory.query
        .filter_by(
            deleted=False
        )
        .order_by(
            DropdownCategory.name
        )
        .all()
    )

    return render_template(
        "admin/dropdowns/index.html",
        categories=categories
    )


@dropdowns_bp.route(
    "/category/create",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def create_category():

    if request.method == "POST":

        existing = (
            DropdownCategory.query
            .filter_by(
                name=request.form.get(
                    "name"
                )
            )
            .first()
        )

        if existing:

            flash(
                "Category already exists.",
                "warning"
            )

            return redirect(
                url_for(
                    "dropdowns.create_category"
                )
            )

        category = DropdownCategory(

            name=request.form.get(
                "name"
            ),

            description=request.form.get(
                "description"
            ),

            input_type=request.form.get(
                "input_type",
                "dropdown"
            ),

            active=(
                "active"
                in request.form
            )
        )

        db.session.add(
            category
        )

        db.session.commit()

        flash(
            "Category created successfully.",
            "success"
        )

        return redirect(
            url_for(
                "dropdowns.index"
            )
        )

    return render_template(
        "admin/dropdowns/create_category.html"
    )


@dropdowns_bp.route(
    "/category/<int:id>"
)
@login_required
@admin_required
def category(id):

    category = (
        DropdownCategory.query
        .get_or_404(id)
    )

options = (
    DropdownOption.query
    .filter_by(
        category_id=id,
        deleted=False
    )
    .order_by(
        DropdownOption.sort_order,
        DropdownOption.value
    )
    .all()
)
    return render_template(
        "admin/dropdowns/category.html",
        category=category,
        options=options
    )


@dropdowns_bp.route(
    "/category/<int:id>/edit",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_category(id):

    category = (
        DropdownCategory.query
        .get_or_404(id)
    )

    if request.method == "POST":

        category.name = (
            request.form.get(
                "name"
            )
        )

        category.description = (
            request.form.get(
                "description"
            )
        )

        category.input_type = (
            request.form.get(
                "input_type",
                "dropdown"
            )
        )

        category.active = (
            "active"
            in request.form
        )

        db.session.commit()

        flash(
            "Category updated.",
            "success"
        )

        return redirect(
            url_for(
                "dropdowns.index"
            )
        )

    return render_template(
        "admin/dropdowns/edit_category.html",
        category=category
    )


@dropdowns_bp.route(
    "/category/<int:id>/delete",
    methods=["POST"]
)
@login_required
@admin_required
def delete_category(id):

    category = (
        DropdownCategory.query
        .get_or_404(id)
    )

    category.deleted = True

    category.deleted_at = (
        datetime.utcnow()
    )

    db.session.commit()

    flash(
        "Category deleted.",
        "success"
    )

    return redirect(
        url_for(
            "dropdowns.index"
        )
    )


@dropdowns_bp.route(
    "/option/create/<int:category_id>",
    methods=["POST"]
)
@login_required
@admin_required
def create_option(category_id):

    category = (
        DropdownCategory.query
        .get_or_404(category_id)
    )

    option = DropdownOption(

        category_id=category.id,

        value=request.form.get(
            "value"
        ),

        description=request.form.get(
            "description"
        ),

        sort_order=int(
            request.form.get(
                "sort_order",
                0
            )
        ),

        active=(
            "active"
            in request.form
        )
    )

    db.session.add(
        option
    )

    db.session.commit()

    flash(
        "Option created.",
        "success"
    )

    return redirect(
        url_for(
            "dropdowns.category",
            id=category_id
        )
    )


@dropdowns_bp.route(
    "/option/<int:id>/edit",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_option(id):

    option = (
        DropdownOption.query
        .get_or_404(id)
    )

    if request.method == "POST":

        option.value = (
            request.form.get(
                "value"
            )
        )

        option.description = (
            request.form.get(
                "description"
            )
        )

        option.sort_order = int(
            request.form.get(
                "sort_order",
                0
            )
        )

        option.active = (
            "active"
            in request.form
        )

        db.session.commit()

        flash(
            "Option updated.",
            "success"
        )

        return redirect(
            url_for(
                "dropdowns.category",
                id=option.category_id
            )
        )

    return render_template(
        "admin/dropdowns/edit_option.html",
        option=option
    )


@dropdowns_bp.route(
    "/option/<int:id>/delete",
    methods=["POST"]
)
@login_required
@admin_required
def delete_option(id):

    option = (
        DropdownOption.query
        .get_or_404(id)
    )

    category_id = (
        option.category_id
    )

    option.deleted = True

    option.deleted_at = (
        datetime.utcnow()
    )

    db.session.commit()

    flash(
        "Option deleted.",
        "success"
    )

    return redirect(
        url_for(
            "dropdowns.category",
            id=category_id
        )
    )


@dropdowns_bp.route(
    "/category/<int:id>/toggle",
    methods=["POST"]
)
@login_required
@admin_required
def toggle_category(id):

    category = (
        DropdownCategory.query
        .get_or_404(id)
    )

    category.active = (
        not category.active
    )

    db.session.commit()

    flash(
        "Category status updated.",
        "success"
    )

    return redirect(
        url_for(
            "dropdowns.index"
        )
    )


@dropdowns_bp.route(
    "/option/<int:id>/toggle",
    methods=["POST"]
)
@login_required
@admin_required
def toggle_option(id):

    option = (
        DropdownOption.query
        .get_or_404(id)
    )

    option.active = (
        not option.active
    )

    db.session.commit()

    flash(
        "Option status updated.",
        "success"
    )

    return redirect(
        url_for(
            "dropdowns.category",
            id=option.category_id
        )
    )
