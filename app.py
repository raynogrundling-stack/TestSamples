import os
import time
import models
from routes.main import main_bp
from flask import (
    Flask,
    g,
    request,
    redirect,
    url_for
)
from config import config
from extensions import (
    db,
    migrate,
    login_manager,
    bcrypt
)
from models.user import User
from models.system_settings import (SystemSettings)
from services.metrics_service import (MetricsService)
from routes.health import health_bp
from routes.auth import auth_bp
from routes.users import users_bp
from routes.setup import setup_bp
from routes.settings import settings_bp
from routes.backups import backups_bp
from routes.restore import restore_bp
from routes.monitoring import monitoring_bp
from routes.submissions import submissions_bp
from routes.audit import audit_bp
from routes.email_monitoring import (email_monitoring_bp)
from routes.imports import imports_bp
from routes.exports import exports_bp
from routes.migrations import migrations_bp
from routes.errors import (register_error_handlers)
from routes.customers import customers_bp
from routes.dropdowns import dropdowns_bp
def create_app(config_name=None):
    config_name = (
        config_name
        or
        os.getenv(
            "FLASK_ENV",
            "production"
        )
    )
    app = Flask(__name__)
    app.config.from_object(
        config[config_name]
    )
    #
    # Extensions
    #
    db.init_app(app)
    migrate.init_app(
        app,
        db
    )
    login_manager.init_app(
        app
    )
    bcrypt.init_app(
        app
    )
    #
    # Temporary bootstrap
    #
    # Remove once Alembic
    # migrations are working
    #
    # Global template data
    #
    @app.context_processor
    def inject_settings():
        try:
            settings = (
                SystemSettings.query.first()
            )
        except Exception:
            db.session.rollback()
            settings = None
        return {
            "settings": settings
        }
    register_blueprints(app)
    register_error_handlers(app)
    register_login_manager()
    register_request_hooks(app)
    return app
def register_blueprints(app):
    blueprints = [
        main_bp,
        health_bp,
        auth_bp,
        users_bp,
        setup_bp,
        settings_bp,
        backups_bp,
        restore_bp,
        monitoring_bp,
        submissions_bp,
        audit_bp,
        email_monitoring_bp,
        imports_bp,
        exports_bp,
        migrations_bp,
        customers_bp,
        dropdowns_bp
    ]
    for blueprint in blueprints:
        app.register_blueprint(
            blueprint
        )
def register_login_manager():
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(
            int(user_id)
        )
def register_request_hooks(app):
    @app.before_request
    def before_request():
        g.start_time = time.time()
    @app.after_request
    def after_request(response):
        try:
            MetricsService.record_request(
                endpoint=request.path,
                response_time_ms=int(
                    (
                        time.time()
                        - g.start_time
                    ) * 1000
                ),
                status_code=response.status_code
            )
        except Exception:
            pass
        return response
    @app.before_request
    def enforce_setup():
        public_endpoints = {
            "setup.index",
            "setup.status",
            "auth.login",
            "auth.logout",
            "auth.reset_password",
            "static"
        }
        if request.endpoint in public_endpoints:
            return
        try:
            settings = (
                SystemSettings.query.first()
            )
        except Exception:
            return
        #
        # First run
        #
        if not settings:
            return redirect(
                url_for(
                    "setup.index"
                )
            )
        #
        # Setup incomplete
        #
        if not settings.setup_completed:
            return redirect(
                url_for(
                    "setup.index"
                )
            )
app = create_app()
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )