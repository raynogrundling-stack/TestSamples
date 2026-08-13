from datetime import datetime
from extensions import db
class DropdownCategory(db.Model):
    __tablename__ = "dropdown_categories"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )
    description = db.Column(
        db.String(500)
    )
    active = db.Column(
        db.Boolean,
        default=True
    )
    deleted = db.Column(
        db.Boolean,
        default=False
    )
    deleted_at = db.Column(
        db.DateTime
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
    options = db.relationship(
        "DropdownOption",
        backref="category",
        lazy=True
    )