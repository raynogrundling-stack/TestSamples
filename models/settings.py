from extensions import db


class SystemSettings(db.Model):

    __tablename__ = "settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    logo_file = db.Column(
        db.String(500)
    )

    smtp_server = db.Column(
        db.String(255)
    )

    smtp_port = db.Column(
        db.Integer
    )

    smtp_username = db.Column(
        db.String(255)
    )

    smtp_password = db.Column(
        db.String(255)
    )

    submission_email = db.Column(
        db.String(255)
    )
