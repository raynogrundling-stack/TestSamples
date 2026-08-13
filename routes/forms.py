from flask import Blueprint

forms_bp = Blueprint(
    "forms",
    __name__,
    url_prefix="/forms"
)

@forms_bp.route("/")
def index():
    return "Form List"