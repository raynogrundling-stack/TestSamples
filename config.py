import os


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-me"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        (
            "postgresql://formsuser:"
            "password@postgres/formsdb"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #
    # Default session security
    #
    # Overridden in subclasses
    #

    SESSION_COOKIE_SECURE = False

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_SECURE = False

    WTF_CSRF_ENABLED = True

    UPLOAD_FOLDER = "uploads"

    PDF_FOLDER = "generated/pdfs"

    CSV_FOLDER = "generated/csv"

    BARCODE_FOLDER = "generated/barcodes"

    BACKUP_FOLDER = "/backups"

    MAX_CONTENT_LENGTH = (
        50 * 1024 * 1024
    )

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0"
    )

    CELERY_BROKER_URL = REDIS_URL

    CELERY_RESULT_BACKEND = REDIS_URL

    SMTP_SERVER = os.getenv(
        "SMTP_SERVER"
    )

    SMTP_PORT = int(
        os.getenv(
            "SMTP_PORT",
            587
        )
    )

    SMTP_USERNAME = os.getenv(
        "SMTP_USERNAME"
    )

    SMTP_PASSWORD = os.getenv(
        "SMTP_PASSWORD"
    )

    PROMETHEUS_ENABLED = True

    GRAFANA_ENABLED = True

    SESSION_TIMEOUT_MINUTES = int(
        os.getenv(
            "SESSION_TIMEOUT_MINUTES",
            30
        )
    )

    ITEMS_PER_PAGE = 50


class DevelopmentConfig(Config):

    DEBUG = True

    SESSION_COOKIE_SECURE = False

    REMEMBER_COOKIE_SECURE = False


class ProductionConfig(Config):

    DEBUG = False

    TESTING = False

    #
    # HTTPS required
    #

    SESSION_COOKIE_SECURE = True

    REMEMBER_COOKIE_SECURE = True


class TestingConfig(Config):

    TESTING = True

    WTF_CSRF_ENABLED = False

    SESSION_COOKIE_SECURE = False

    REMEMBER_COOKIE_SECURE = False

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"
    )


config = {

    "development":
    DevelopmentConfig,

    "production":
    ProductionConfig,

    "testing":
    TestingConfig

}