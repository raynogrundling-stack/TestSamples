from datetime import datetime

from flask import current_app
from flask_login import UserMixin

from itsdangerous import (
    URLSafeTimedSerializer
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db


class User(
    UserMixin,
    db.Model
):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    surname = db.Column(
        db.String(255)
    )

    contact_number = db.Column(
        db.String(50)
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )

    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
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
            f"<User "
            f"{self.email}>"
        )

    #
    # Flask-Login
    #

    def is_active(self):
        return self.active

    #
    # Roles
    #

    def is_admin(self):
        return self.role == "admin"

    #
    # Password Helpers
    #

    def set_password(
        self,
        password
    ):
        self.password_hash = (
            generate_password_hash(
                password
            )
        )

    def check_password(
        self,
        password
    ):
        return check_password_hash(
            self.password_hash,
            password
        )

    #
    # Password Reset
    #

    def generate_reset_token(self):

        serializer = URLSafeTimedSerializer(
            current_app.config[
                "SECRET_KEY"
            ]
        )

        return serializer.dumps(
            self.email,
            salt=current_app.config[
                "SECURITY_PASSWORD_SALT"
            ]
        )

    @staticmethod
    def verify_reset_token(
        token,
        expiry=3600
    ):

        serializer = URLSafeTimedSerializer(
            current_app.config[
                "SECRET_KEY"
            ]
        )

        try:

            email = serializer.loads(
                token,
                salt=current_app.config[
                    "SECURITY_PASSWORD_SALT"
                ],
                max_age=expiry
            )

        except Exception:
            return None

        return User.query.filter_by(
            email=email
        ).first()

    #
    # Convenience Methods
    #

    @staticmethod
    def get_admins():

        return User.query.filter_by(
            role="admin"
        ).all()

    @staticmethod
    def admin_exists():

        return (
            User.query.filter_by(
                role="admin"
            ).count() > 0
        )
