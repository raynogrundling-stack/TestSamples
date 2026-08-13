from datetime import datetime

from extensions import db


class Submission(db.Model):

    __tablename__ = "submissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id")
    )

    order_reference = db.Column(
        db.String(100),
        unique=True
    )
    contact_name = db.Column(
        db.String(255)
    )

    contact_surname = db.Column(
        db.String(255)
    )

    contact_phone = db.Column(
        db.String(100)
    )

    contact_email = db.Column(
        db.String(255)
    )

    company_submission_email = db.Column(
        db.String(255)
    )
    sample_number = db.Column(
        db.String(100),
        unique=True
    )

    customer_name = db.Column(
        db.String(255)
    )

    sample_description = db.Column(
        db.Text
    )

    sample_type = db.Column(
        db.String(100)
    )

    test_required = db.Column(
        db.String(255)
    )

    results_email = db.Column(
        db.String(255)
    )

    status = db.Column(
        db.String(50),
        default="Draft"
    )

    submitted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    field_data = db.Column(
        db.JSON
    )

    comments = db.Column(
        db.Text
    )

    pdf_path = db.Column(
        db.String(500)
    )

    csv_path = db.Column(
        db.String(500)
    )

    barcode_file = db.Column(
        db.String(500)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="submissions"
    )

    customer = db.relationship(
        "Customer",
        backref="submissions"
    )
