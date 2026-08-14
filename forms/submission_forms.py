# forms/submission_forms.py

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    BooleanField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    Email,
    Length
)


class SubmissionForm(FlaskForm):
    """
    Main submission form used to create
    laboratory sample submissions.
    """

    customer_id = SelectField(
        "Customer",
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    #
    # Contact Person Details
    #

    contact_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    contact_surname = StringField(
        "Surname",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    contact_phone = StringField(
        "Contact Number",
        validators=[
            Optional(),
            Length(max=50)
        ]
    )

    contact_email = StringField(
        "Contact Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=255)
        ]
    )

    #
    # Sample Information
    #

    sample_description = TextAreaField(
        "Sample Description",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=2000
            )
        ]
    )

    order_reference = StringField(
        "Order Reference",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    sample_type = StringField(
        "Sample Type",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    test_required = StringField(
        "Test Required",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    results_email = StringField(
        "Results Email",
        validators=[
            Optional(),
            Email(),
            Length(max=255)
        ]
    )

    comments = TextAreaField(
        "Comments",
        validators=[
            Optional(),
            Length(max=4000)
        ]
    )

    #
    # Output Options
    #

    generate_pdf = BooleanField(
        "Generate PDF",
        default=True
    )

    generate_csv = BooleanField(
        "Generate CSV",
        default=True
    )

    send_email = BooleanField(
        "Email Results",
        default=True
    )

    submit = SubmitField(
        "Submit"
    )


class DraftSubmissionForm(SubmissionForm):
    """
    Draft version of the submission form.
    """

    save_draft = SubmitField(
        "Save Draft"
    )
