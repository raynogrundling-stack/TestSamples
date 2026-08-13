from datetime import datetime

from extensions import db


class CustomerEmail(db.Model):

    __tablename__ = "customer_emails"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "customers.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    email_address = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    recipient_name = db.Column(
        db.String(255),
        nullable=True
    )

    is_primary = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    deleted_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):

        return (
            f"<CustomerEmail "
            f"{self.email_address}>"
        )