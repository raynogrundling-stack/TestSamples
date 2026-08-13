from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from datetime import datetime
from flask_login import (
    login_required,
    current_user
)
from extensions import db
from models.customer import (
    Customer
)
customers_bp = Blueprint(
    "customers",
    __name__,
    url_prefix="/admin/customers"
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
@customers_bp.route("/")
@login_required
@admin_required
def index():
    customers = (
        Customer.query
        .filter_by(
            deleted=False
        )
        .order_by(
            Customer.customer_name
        )
        .all()
    )
    return render_template(
        "admin/customers/index.html",
        customers=customers
    )
@customers_bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    if request.method == "POST":
        customer = Customer(
            customer_name=request.form.get(
                "customer_name"
            ),
            customer_code=request.form.get(
                "customer_code"
            ),
            contact_number=request.form.get(
                "contact_number"
            ),
            active=True
        )
        db.session.add(
            customer
        )
        db.session.commit()
        flash(
            "Customer created.",
            "success"
        )
        return redirect(
            url_for(
                "customers.index"
            )
        )
    return render_template(
        "admin/customers/create.html"
    )
@customers_bp.route("/<int:id>/edit",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit(id):
    customer = (
        Customer.query.get_or_404(
            id
        )
    )
    if request.method == "POST":
        customer.customer_name = (
            request.form.get(
                "customer_name"
            )
        )
        customer.customer_code = (
            request.form.get(
                "customer_code"
            )
        )
        customer.contact_number = (
            request.form.get(
                "contact_number"
            )
        )
        customer.active = (
            "active" in request.form
        )
        db.session.commit()
        flash(
            "Customer updated.",
            "success"
        )
        return redirect(
            url_for(
                "customers.index"
            )
        )
    return render_template(
        "admin/customers/edit.html",
        customer=customer
    )
@customers_bp.route(
    "/<int:id>/delete",
    methods=["POST"]
)
@login_required
@admin_required
def delete(id):
    customer = (
        Customer.query.get_or_404(
            id
        )
    )
    customer.deleted = True
    customer.deleted_at = (
        datetime.utcnow()
    )
    db.session.commit()
    flash(
        "Customer removed.",
        "success"
    )
    return redirect(
        url_for(
            "customers.index"
        )
    )