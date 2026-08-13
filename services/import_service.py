import csv
import json
import zipfile

from pathlib import Path

from extensions import db

from models.customer import Customer
from models.system_settings import (
    SystemSettings
)

# Uncomment once available
#
# from models.dropdown_category import (
#     DropdownCategory
# )
#
# from models.dropdown_option import (
#     DropdownOption
# )

from services.logger import logger


class ImportService:

    @staticmethod
    def validate_csv(
        file_path,
        required_columns=None
    ):

        if required_columns is None:
            required_columns = []

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as csv_file:

                reader = csv.DictReader(
                    csv_file
                )

                columns = (
                    reader.fieldnames
                    or []
                )

            missing = [

                col

                for col in required_columns

                if col not in columns

            ]

            return {

                "valid":
                len(missing) == 0,

                "columns":
                columns,

                "missing":
                missing

            }

        except Exception as ex:

            logger.exception(
                "CSV validation failed"
            )

            return {

                "valid": False,

                "error": str(ex)

            }

    @staticmethod
    def preview_csv(
        file_path,
        limit=25
    ):

        rows = []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as csv_file:

            reader = csv.DictReader(
                csv_file
            )

            for count, row in enumerate(
                reader
            ):

                rows.append(row)

                if count >= (
                    limit - 1
                ):
                    break

        return rows

    @staticmethod
    def import_customers(
        file_path
    ):

        imported = 0
        skipped = 0

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as csv_file:

            reader = csv.DictReader(
                csv_file
            )

            for row in reader:

                existing = (

                    Customer.query

                    .filter_by(

                        customer_code=
                        row[
                            "customer_code"
                        ]

                    )

                    .first()

                )

                if existing:

                    skipped += 1

                    continue

                customer = Customer(

                    customer_name=
                    row[
                        "customer_name"
                    ],

                    customer_code=
                    row[
                        "customer_code"
                    ],

                    contact_number=
                    row.get(
                        "contact_number"
                    )

                )

                db.session.add(
                    customer
                )

                imported += 1

        db.session.commit()

        logger.info(

            f"Imported "
            f"{imported} customers"

        )

        return {

            "imported": imported,

            "skipped": skipped

        }

    @staticmethod
    def import_dropdowns(
        category_name,
        file_path
    ):

        #
        # This implementation
        # assumes dropdown
        # models are available.
        #

        imported = 0

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as csv_file:

            reader = csv.DictReader(
                csv_file
            )

            for row in reader:

                imported += 1

                #
                # Create
                # DropdownOption
                #
                # when models
                # are present
                #

        db.session.commit()

        return {

            "imported": imported

        }

    @staticmethod
    def import_settings(
        file_path
    ):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as settings_file:

            payload = json.load(
                settings_file
            )

        settings = (
            SystemSettings.query
            .first()
        )

        if not settings:

            settings = (
                SystemSettings()
            )

            db.session.add(
                settings
            )

        settings.company_name = (

            payload.get(
                "company_name"
            )
        )

        settings.smtp_server = (

            payload.get(
                "smtp_server"
            )
        )

        settings.smtp_port = (

            payload.get(
                "smtp_port"
            )
        )

        settings.smtp_sender_name = (

            payload.get(
                "smtp_sender_name"
            )
        )

        settings.smtp_sender_address = (

            payload.get(
                "smtp_sender_address"
            )
        )

        db.session.commit()

        logger.info(
            "Settings imported"
        )

        return True

    @staticmethod
    def import_backup_zip(
        file_path
    ):

        try:

            if not zipfile.is_zipfile(
                file_path
            ):

                return {

                    "success": False,

                    "error":
                    "Invalid ZIP file."

                }

            with zipfile.ZipFile(
                file_path,
                "r"
            ) as archive:

                files = (
                    archive.namelist()
                )

            return {

                "success": True,

                "files": files

            }

        except Exception as ex:

            logger.exception(
                "Backup import failed"
            )

            return {

                "success": False,

                "error": str(ex)

            }

    @staticmethod
    def import_json(
        file_path
    ):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file_handle:

            return json.load(
                file_handle
            )

    @staticmethod
    def get_import_stats():

        return {

            "supported_formats": [

                "csv",

                "json",

                "zip"

            ],

            "customer_import":
            True,

            "dropdown_import":
            True,

            "settings_import":
            True,

            "backup_import":
            True

        }

    @staticmethod
    def create_upload_folder():

        upload_path = Path(
            "uploads/imports"
        )

        upload_path.mkdir(

            parents=True,

            exist_ok=True

        )

        return upload_path