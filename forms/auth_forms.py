from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )
    submit = SubmitField(
        "Login"
    )
class RegisterForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=255)
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )
    submit = SubmitField(
        "Register"
    )
class RequestResetForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )
    submit = SubmitField(
        "Request Password Reset"
    )
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )
    submit = SubmitField(
        "Reset Password"
    )