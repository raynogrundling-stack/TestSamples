from datetime import datetime

from models.sequence import Sequence

from extensions import db


class ReferenceService:

    @staticmethod
    def next_value(name):

        sequence = (

            Sequence.query
            .filter_by(
                name=name
            )
            .first()

        )

        value = sequence.next_value

        sequence.next_value += 1

        db.session.commit()

        return value

    @staticmethod
    def generate_reference():

        number = (

            ReferenceService
            .next_value(
                "ORDER_REF"
            )

        )

        return (
            f"REF{number:06d}"
        )

    @staticmethod
    def generate_sample_number(
        customer_code
    ):

        number = (

            ReferenceService
            .next_value(
                "SAMPLE_NO"
            )

        )

        return (
            f"SAMP"
            f"{customer_code}"
            f"{number:06d}"
        )