from flask import (
    render_template,
    request,
    jsonify
)

from services.logger import logger

from extensions import db
def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):

        if request.path.startswith("/api"):

            return jsonify({
                "success": False,
                "error": "Bad Request"
            }), 400

        return render_template(
            "errors/400.html"
        ), 400

    @app.errorhandler(403)
    def forbidden(error):

        if request.path.startswith("/api"):

            return jsonify({
                "success": False,
                "error": "Forbidden"
            }), 403

        return render_template(
            "errors/403.html"
        ), 403

    @app.errorhandler(404)
    def not_found(error):

        if request.path.startswith("/api"):

            return jsonify({
                "success": False,
                "error": "Not Found"
            }), 404

        return render_template(
            "errors/404.html"
        ), 404

    @app.errorhandler(500)
    def internal_error(error):

        try:
            logger.exception(
                "Unhandled application error"
            )
        except Exception:
            pass

        if request.path.startswith("/api"):

            return jsonify({
                "success": False,
                "error": "Internal Server Error"
            }), 500

        return render_template(
            "errors/500.html"
        ), 500

    @app.errorhandler(Exception)
    def unhandled_exception(error):

        try:
            logger.exception(
                str(error)
            )
        except Exception:
            pass

        if request.path.startswith("/api"):

            return jsonify({
                "success": False,
                "error": str(error)
            }), 500
        db.session.rollback()
        return render_template(
            "errors/500.html",
            error=error
        ), 500