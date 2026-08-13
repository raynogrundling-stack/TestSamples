from flask import (
    Blueprint,
    jsonify
)

from datetime import datetime

health_bp = Blueprint(
    "health",
    __name__,
    url_prefix="/health"
)


@health_bp.route("/")
def health():

    return jsonify({

        "status": "healthy",

        "timestamp":
        datetime.utcnow().isoformat()

    })


@health_bp.route("/live")
def live():

    return jsonify({

        "status": "alive",

        "service":
        "laboratory_forms"

    })


@health_bp.route("/ready")
def ready():

    return jsonify({

        "ready": True

    })