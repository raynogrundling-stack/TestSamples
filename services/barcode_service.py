from pathlib import Path

import barcode

from barcode.writer import (
    ImageWriter
)


class BarcodeService:

    BARCODE_FOLDER = (
        "generated/barcodes"
    )

    @staticmethod
    def generate(
        sample_number
    ):

        Path(
            BarcodeService.BARCODE_FOLDER
        ).mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            f"{BarcodeService.BARCODE_FOLDER}/"
            f"{sample_number}"

        )

        code = barcode.get(

            "code128",

            sample_number,

            writer=ImageWriter()

        )

        return code.save(
            filepath
        )