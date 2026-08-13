from pathlib import Path

from flask import render_template

from weasyprint import HTML


class PDFService:

    OUTPUT_FOLDER = (
        "generated/pdfs"
    )

    @staticmethod
    def generate_pdf(submission):

        Path(
            PDFService.OUTPUT_FOLDER
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            f"{PDFService.OUTPUT_FOLDER}/"
            f"{submission.sample_number}.pdf"
        )

        html = render_template(
            "pdf/submission_pdf.html",
            submission=submission,
            barcode_path=submission.barcode_file
        )

        HTML(
            string=html,
            base_url="."
        ).write_pdf(output_file)

        return output_file