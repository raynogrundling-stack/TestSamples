from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    BooleanField,
    SubmitField,
    PasswordField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Optional,
    EqualTo
)


class UserCreateForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            DataRequired()
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("admin", "Admin"),
            ("manager", "Manager"),
            ("user", "User"),
            ("auditor", "Auditor")
        ]
    )

    active = BooleanField(
        "Active"
    )

    password = PasswordField(
        "Password",
        validators=[
            Optional()
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            Optional(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField(
        "Save"
    )


class UserEditForm(UserCreateForm):
    pass