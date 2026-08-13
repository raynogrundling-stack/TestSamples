from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    request
)

from flask_login import (
    login_required,
    current_user
)

from models.email_queue import (
    EmailQueue
)

from services.email_queue_service import (
    EmailQueueService
)

from services.audit_service import (
    AuditService
)

from extensions import db


email_monitoring_bp = Blueprint(
    "email_monitoring",
    __name__,
    url_prefix="/admin/emails"
)


def admin_required(func):

    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not current_user.is_admin():

            flash(
                "Access denied.",
                "danger"
            )

            return redirect("/")

        return func(
            *args,
            **kwargs
        )

    return wrapper


@email_monitoring_bp.route("/")
@login_required
@admin_required
def dashboard():

    stats = EmailQueueService.get_stats()

    return render_template(
        "admin/emails/dashboard.html",
        stats=stats
    )


@email_monitoring_bp.route("/queue")
@login_required
@admin_required
def queue():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    pagination = (

        EmailQueue.query

        .filter_by(
            deleted=False
        )

        .order_by(
            EmailQueue.created_at.desc()
        )

        .paginate(
            page=page,
            per_page=50,
            error_out=False
        )

    )

    return render_template(

        "admin/emails/queue.html",

        emails=pagination.items,

        pagination=pagination

    )


@email_monitoring_bp.route("/failed")
@login_required
@admin_required
def failed():

    emails = (
        EmailQueueService
        .failed_emails()
    )

    return render_template(

        "admin/emails/failed.html",

        emails=emails

    )


@email_monitoring_bp.route(
    "/view/<int:email_id>"
)
@login_required
@admin_required
def view(email_id):

    email = EmailQueue.query.get_or_404(
        email_id
    )

    return render_template(

        "admin/emails/view.html",

        email=email

    )


@email_monitoring_bp.route(
    "/retry/<int:email_id>",
    methods=["POST"]
)
@login_required
@admin_required
def retry(email_id):

    email = EmailQueue.query.get_or_404(
        email_id
    )

    email.status = "PENDING"

    db.session.commit()

    AuditService.log(

        action="EMAIL_RETRY",

        user_id=current_user.id,

        object_type="EMAIL",

        object_id=str(email.id)

    )

    flash(
        "Email queued for retry.",
        "success"
    )

    return redirect(
        url_for(
            "email_monitoring.view",
            email_id=email.id
        )
    )


@email_monitoring_bp.route(
    "/delete/<int:email_id>",
    methods=["POST"]
)
@login_required
@admin_required
def delete(email_id):

    success = (
        EmailQueueService
        .mark_deleted(email_id)
    )

    if success:

        AuditService.log(

            action="EMAIL_DELETED",

            user_id=current_user.id,

            object_type="EMAIL",

            object_id=str(email_id)

        )

        flash(
            "Email deleted.",
            "success"
        )

    else:

        flash(
            "Email not found.",
            "danger"
        )

    return redirect(
        url_for(
            "email_monitoring.queue"
        )
    )


@email_monitoring_bp.route(
    "/api/stats"
)
@login_required
@admin_required
def api_stats():

    return jsonify(
        EmailQueueService.get_stats()
    )


@email_monitoring_bp.route(
    "/api/recent"
)
@login_required
@admin_required
def api_recent():

    emails = (

        EmailQueue.query

        .filter_by(
            deleted=False
        )

        .order_by(
            EmailQueue.created_at.desc()
        )

        .limit(20)

        .all()

    )

    return jsonify([

        {
            "id":
            email.id,

            "subject":
            email.subject,

            "status":
            email.status,

            "recipient_count":
            email.recipient_count,

            "created_at":
            str(email.created_at)

        }

        for email in emails

    ])