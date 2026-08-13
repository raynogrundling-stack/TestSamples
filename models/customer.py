from datetime import datetime

from extensions import db


class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_name = db.Column(
        db.String(255),
        nullable=False
    )

    customer_code = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    contact_number = db.Column(
        db.String(100)
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    deleted_at = db.Column(
        db.DateTime,
        nullable=True
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

    def __repr__(self):

        return (
            f"<Customer "
            f"{self.customer_name}>"
        )