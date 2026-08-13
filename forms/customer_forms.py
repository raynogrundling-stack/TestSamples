from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    Length,
    Email,
    ValidationError
)


class CustomerForm(FlaskForm):

    customer_name = StringField(
        "Customer Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=255
            )
        ]
    )

    customer_code = StringField(
        "Customer Code",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=100
            )
        ]
    )

    contact_number = StringField(
        "Contact Number",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    contact_person = StringField(
        "Contact Person",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    address = TextAreaField(
        "Address",
        validators=[
            Optional(),
            Length(max=2000)
        ]
    )

    result_emails = TextAreaField(
        "Results Email Addresses",
        validators=[
            Optional(),
            Length(max=4000)
        ],
        description=(
            "Enter one email address per line."
        )
    )

    notes = TextAreaField(
        "Notes",
        validators=[
            Optional(),
            Length(max=4000)
        ]
    )

    active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField(
        "Save Customer"
    )

    def validate_result_emails(
        self,
        field
    ):

        if not field.data:
            return

        emails = [

            line.strip()

            for line in

            field.data.splitlines()

            if line.strip()

        ]

        for email in emails:

            try:

                Email()(
                    self,
                    type(
                        "obj",
                        (),
                        {"data": email}
                    )()
                )

            except Exception:

                raise ValidationError(

                    f"Invalid email: {email}"

                )


class CustomerCreateForm(
    CustomerForm
):
    pass


class CustomerEditForm(
    CustomerForm
):
    pass


class CustomerSearchForm(
    FlaskForm
):

    customer_name = StringField(
        "Customer Name"
    )

    customer_code = StringField(
        "Customer Code"
    )

    active = BooleanField(
        "Active Only"
    )

    submit = SubmitField(
        "Search"
    )


class CustomerImportForm(
    FlaskForm
):

    submit = SubmitField(
        "Import Customers"
    )


class CustomerExportForm(
    FlaskForm
):

    include_inactive = BooleanField(
        "Include Inactive Customers"
    )

    submit = SubmitField(
        "Export Customers"
    )