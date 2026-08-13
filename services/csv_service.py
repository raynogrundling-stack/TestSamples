import csv

from pathlib import Path


class CSVService:

    OUTPUT_FOLDER = (
        "generated/csv"
    )

    @staticmethod
    def generate_csv(submission):

        Path(
            CSVService.OUTPUT_FOLDER
        ).mkdir(

            parents=True,

            exist_ok=True

        )

        output_file = (

            f"{CSVService.OUTPUT_FOLDER}/"
            f"{submission.sample_number}.csv"

        )

        with open(

            output_file,

            "w",

            newline="",

            encoding="utf-8"

        ) as csv_file:

            writer = csv.writer(
                csv_file
            )

            writer.writerow([
                "Reference"
            ])

            writer.writerow([
                submission.order_reference
            ])

            writer.writerow([
                "Sample Number"
            ])

            writer.writerow([
                submission.sample_number
            ])

            writer.writerow([
                "Customer"
            ])

            writer.writerow([
                submission.customer_name
            ])

        return output_file