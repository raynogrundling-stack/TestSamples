from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db

from models.submission import Submission
from models.customer import Customer

from forms.submission_forms import (
    SubmissionForm
)

from services.reference_service import (
    ReferenceService
)

from services.pdf_service import (
    PDFService
)

from services.csv_service import (
    CSVService
)

from services.barcode_service import (
    BarcodeService
)

submissions_bp = Blueprint(
    "submissions",
    __name__,
    url_prefix="/submissions"
)


@submissions_bp.route("/")
@login_required
def dashboard():

    stats = {
        "total": Submission.query.count(),
        "completed": Submission.query.filter_by(
            status="Completed"
        ).count(),
        "drafts": Submission.query.filter_by(
            status="Draft"
        ).count(),
        "failed": Submission.query.filter_by(
            status="Failed"
        ).count()
    }

    return render_template(
        "forms/dashboard.html",
        stats=stats
    )


@submissions_bp.route("/history")
@login_required
def history():

    submissions = (
        Submission.query
        .order_by(
            Submission.id.desc()
        )
        .all()
    )

    return render_template(
        "forms/submission_history.html",
        submissions=submissions
    )


@submissions_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
def create():

    form = SubmissionForm()

    customers = Customer.query.order_by(
        Customer.customer_name
    ).all()

    form.customer_id.choices = [
        (
            c.id,
            c.customer_name
        )
        for c in customers
    ]

    if form.validate_on_submit():

        customer = Customer.query.get(
            form.customer_id.data
        )

        order_reference = (
            ReferenceService
            .generate_reference()
        )

        sample_number = (
            ReferenceService.generate_sample_number(
                customer.customer_code
            )
        )

        submission = Submission(
            user_id=current_user.id,
            customer_id=customer.id,
            customer_name=customer.customer.name,
            order_reference=order_reference,
            sample_number=sample_number,
            sample_description=form.sample_description.data,
            sample_type=form.sample_type.data,
            test_required=form.test_required.data,
            results_email=form.results_email.data,
            comments=form.comments.data,
            status="Submitted",
            submitted_at=datetime.utcnow()
        )

        barcode_file = (
            BarcodeService.generate(
                sample_number
            )
        )

        submission.barcode_file = (
            barcode_file
        )

        db.session.add(
            submission
        )

        db.session.commit()

        if form.generate_pdf.data:

            submission.pdf_path = (
                PDFService.generate_pdf(
                    submission
                )
            )

        if form.generate_csv.data:

            submission.csv_path = (
                CSVService.generate_csv(
                    submission
                )
            )

        db.session.commit()

        flash(
            "Submission created successfully.",
            "success"
        )

        return redirect(
            url_for(
                "submissions.detail",
                submission_id=submission.id
            )
        )

    return render_template(
        "forms/submission_form.html",
        form=form
    )


@submissions_bp.route(
    "/<int:submission_id>"
)
@login_required
def detail(submission_id):

    submission = (
        Submission.query.get_or_404(
            submission_id
        )
    )

    return render_template(
        "forms/submission_detail.html",
        submission=submission
    )


@submissions_bp.route(
    "/drafts"
)
@login_required
def drafts():

    submissions = (
        Submission.query
        .filter_by(
            status="Draft"
        )
        .all()
    )

    return render_template(
        "forms/drafts.html",
        submissions=submissions
    )


@submissions_bp.route(
    "/pdf/<int:submission_id>"
)
@login_required
def pdf(submission_id):

    submission = (
        Submission.query.get_or_404(
            submission_id
        )
    )

    if not submission.pdf_path:
        flash(
            "PDF not available.",
            "warning"
        )
        return redirect(
            url_for(
                "submissions.detail",
                submission_id=submission.id
            )
        )

    return send_file(
        submission.pdf_path
    )


@submissions_bp.route(
    "/csv/<int:submission_id>"
)
@login_required
def csv(submission_id):

    submission = (
        Submission.query.get_or_404(
            submission_id
        )
    )

    if not submission.csv_path:
        flash(
            "CSV not available.",
            "warning"
        )
        return redirect(
            url_for(
                "submissions.detail",
                submission_id=submission.id
            )
        )

    return send_file(
        submission.csv_path
    )


@submissions_bp.route(
    "/barcode/<int:submission_id>"
)
@login_required
def barcode(submission_id):

    submission = (
        Submission.query.get_or_404(
            submission_id
        )
    )

    return send_file(
        submission.barcode_file
    )