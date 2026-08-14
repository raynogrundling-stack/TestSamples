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

    #
    # Field Type
    #
    # dropdown  = single select
    # checklist = multiple select
    #

    input_type = db.Column(
        db.String(20),
        nullable=False,
        default="dropdown"
    )

    active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    deleted_at = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    options = db.relationship(
        "DropdownOption",
        backref="category",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<DropdownCategory "
            f"{self.name}>"
        )

    @property
    def is_dropdown(self):

        return (
            self.input_type
            == "dropdown"
        )

    @property
    def is_checklist(self):

        return (
            self.input_type
            == "checklist"
        )

    def active_options(self):

        return [
            option
            for option in self.options
            if (
                option.active
                and
                not option.deleted
            )
        ]
