from flask import (
    Blueprint,
    render_template,
    jsonify,
    redirect,
    flash
)
from flask_login import (
    login_required,
    current_user
)
from models.failure_log import (
    FailureLog
)
from services.monitoring_service import (
    MonitoringService
)
from services.metrics_service import (
    MetricsService
)
monitoring_bp = Blueprint(
    "monitoring",
    __name__,
    url_prefix="/admin/monitoring"
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
@monitoring_bp.route("/")
@login_required
@admin_required
def overview():
    health = (
        MonitoringService
        .system_health()
    )
    metrics = (
        MetricsService
        .summary()
    )
    return render_template(
        "admin/monitoring/overview.html",
        health=health,
        metrics=metrics
    )
@monitoring_bp.route("/services")
@login_required
@admin_required
def services():
    services = (
        MonitoringService
        .service_status()
    )
    return render_template(
        "admin/monitoring/services.html",
        services=services
    )
@monitoring_bp.route("/metrics")
@login_required
@admin_required
def metrics():
    metrics = (
        MetricsService
        .summary()
    )
    return render_template(
        "admin/monitoring/metrics.html",
        metrics=metrics
    )
@monitoring_bp.route("/failures")
@login_required
@admin_required
def failures():
    failures = (
        FailureLog.query
        .order_by(
            FailureLog.created_at.desc()
        )
        .limit(500)
        .all()
    )
    return render_template(
        "admin/monitoring/failures.html",
        failures=failures
    )
@monitoring_bp.route("/uptime")
@login_required
@admin_required
def uptime():
    uptime = (
        MonitoringService
        .uptime()
    )
    return render_template(
        "admin/monitoring/uptime.html",
        uptime=uptime
    )
@monitoring_bp.route("/api/health")
@login_required
@admin_required
def api_health():
    return jsonify(
        MonitoringService.system_health()
    )
@monitoring_bp.route("/api/services")
@login_required
@admin_required
def api_services():
    return jsonify(
        MonitoringService.service_status()
    )
@monitoring_bp.route("/api/metrics")
@login_required
@admin_required
def api_metrics():
    return jsonify(
        MetricsService.summary()
    )