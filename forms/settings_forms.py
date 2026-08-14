from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    IntegerField,
    PasswordField,
    BooleanField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional,
    NumberRange
)

#
# Shared Settings Forms
#

class CompanySettingsForm(FlaskForm):

    company_name = StringField(
        "Company Name",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    submission_email = StringField(
        "Default Submission Email",
        validators=[
            Optional(),
            Email(),
            Length(max=255)
        ]
    )

    remove_logo = BooleanField(
        "Remove current logo"
    )

    submit = SubmitField(
        "Save Company Settings"
    )


class SMTPSettingsForm(FlaskForm):

    smtp_server = StringField(
        "SMTP Server",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    smtp_port = IntegerField(
        "SMTP Port",
        validators=[
            Optional(),
            NumberRange(
                min=1,
                max=65535
            )
        ],
        default=587
    )

    smtp_username = StringField(
        "SMTP Username",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    smtp_password = PasswordField(
        "SMTP Password",
        validators=[
            Optional()
        ]
    )

    smtp_sender_name = StringField(
        "SMTP Sender Name",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    smtp_sender_address = StringField(
        "SMTP Sender Email",
        validators=[
            Optional(),
            Email()
        ]
    )

    smtp_use_tls = BooleanField(
        "Use TLS",
        default=True
    )

    submit = SubmitField(
        "Save SMTP Settings"
    )


class SecuritySettingsForm(FlaskForm):

    max_login_attempts = IntegerField(
        "Maximum Login Attempts",
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=50
            )
        ],
        default=5
    )

    session_timeout_minutes = IntegerField(
        "Session Timeout (Minutes)",
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=1440
            )
        ],
        default=30
    )

    submit = SubmitField(
        "Save Security Settings"
    )


class MonitoringSettingsForm(FlaskForm):

    monitoring_enabled = BooleanField(
        "Enable Monitoring"
    )

    prometheus_enabled = BooleanField(
        "Enable Prometheus"
    )

    grafana_enabled = BooleanField(
        "Enable Grafana"
    )

    sandbox_enabled = BooleanField(
        "Enable Sandbox Mode",
        default=True
    )

    submit = SubmitField(
        "Save Monitoring Settings"
    )


class PrintingSettingsForm(FlaskForm):

    auto_print_on_submit = BooleanField(
        "Auto Print On Submit"
    )

    enable_browser_printing = BooleanField(
        "Enable Browser Printing"
    )

    submit = SubmitField(
        "Save Printing Settings"
    )


#
# First Run Setup Wizard
#

class SetupWizardForm(FlaskForm):

    sandbox_enabled = BooleanField(
        "Enable Sandbox Mode",
        default=True
    )

    #
    # Company
    #

    company_name = StringField(
        "Company Name",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    submission_email = StringField(
        "Default Submission Email",
        validators=[
            Optional(),
            Email(),
            Length(max=255)
        ]
    )

    #
    # SMTP
    #

    smtp_server = StringField(
        "SMTP Server",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    smtp_port = IntegerField(
        "SMTP Port",
        validators=[
            Optional(),
            NumberRange(
                min=1,
                max=65535
            )
        ],
        default=587
    )

    smtp_username = StringField(
        "SMTP Username",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    smtp_password = PasswordField(
        "SMTP Password",
        validators=[
            Optional()
        ]
    )

    smtp_sender_name = StringField(
        "SMTP Sender Name",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    smtp_sender_address = StringField(
        "SMTP Sender Email",
        validators=[
            Optional(),
            Email()
        ]
    )

    #
    # First Administrator
    #

    admin_name = StringField(
        "Administrator Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=255
            )
        ]
    )

    admin_email = StringField(
        "Administrator Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    admin_password = PasswordField(
        "Administrator Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    submit = SubmitField(
        "Complete Initial Setup"
    )
