from functools import wraps

from flask import (
    flash,
    jsonify
)

from extensions import db


def safe_route(api=False):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            try:

                return func(
                    *args,
                    **kwargs
                )

            except Exception as ex:

                db.session.rollback()

                if api:

                    return jsonify({

                        "success": False,

                        "message": str(ex)

                    }), 500

                flash(
                    str(ex),
                    "danger"
                )

                raise

        return wrapper

    return decorator