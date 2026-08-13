from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    BooleanField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional
)


class UserCreateForm(FlaskForm):

    name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    surname = StringField(
        "Surname",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    contact_number = StringField(
        "Contact Number",
        validators=[
            Optional(),
            Length(max=50)
        ]
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=255)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            Optional(),
            Length(min=8, max=255)
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("user", "User"),
            ("admin", "Administrator")
        ],
        validators=[
            DataRequired()
        ]
    )

    active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField(
        "Create User"
    )


class UserEditForm(FlaskForm):

    name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    surname = StringField(
        "Surname",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    contact_number = StringField(
        "Contact Number",
        validators=[
            Optional(),
            Length(max=50)
        ]
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=255)
        ]
    )

    password = PasswordField(
        "New Password",
        validators=[
            Optional(),
            Length(min=8, max=255)
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("user", "User"),
            ("admin", "Administrator")
        ],
        validators=[
            DataRequired()
        ]
    )

    active = BooleanField(
        "Active"
    )

    submit = SubmitField(
        "Update User"
    )
