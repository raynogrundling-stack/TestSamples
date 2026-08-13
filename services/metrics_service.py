from extensions import db

from models.request_metric import (
    RequestMetric
)


class MetricsService:

    @staticmethod
    def record_request(

        endpoint,

        response_time_ms,

        status_code

    ):

        metric = RequestMetric(

            endpoint=endpoint,

            response_time_ms=
            response_time_ms,

            status_code=
            status_code

        )

        db.session.add(metric)

        db.session.commit()