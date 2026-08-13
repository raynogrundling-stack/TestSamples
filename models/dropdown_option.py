from datetime import datetime
from extensions import db
class DropdownOption(db.Model):
    __tablename__ = "dropdown_options"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "dropdown_categories.id"
        ),
        nullable=False
    )
    value = db.Column(
        db.String(255),
        nullable=False
    )
    description = db.Column(
        db.String(500)
    )
    sort_order = db.Column(
        db.Integer,
        default=0
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