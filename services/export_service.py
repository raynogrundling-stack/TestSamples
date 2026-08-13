import csv
import json
import zipfile

from pathlib import Path

from models.user import User
from models.customer import Customer
from models.submission import Submission
from models.audit_log import AuditLog
from models.system_settings import SystemSettings


class ExportService:

    OUTPUT_FOLDER = "generated/exports"

    @staticmethod
    def ensure_folder():

        Path(
            ExportService.OUTPUT_FOLDER
        ).mkdir(
            parents=True,
            exist_ok=True
        )

    @staticmethod
    def export_customers_csv():

        ExportService.ensure_folder()

        file_path = (
            f"{ExportService.OUTPUT_FOLDER}/"
            f"customers.csv"
        )

        customers = Customer.query.all()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "Customer Name",
                "Customer Code",
                "Contact Number"
            ])

            for customer in customers:

                writer.writerow([
                    customer.customer_name,
                    customer.customer_code,
                    customer.contact_number
                ])

        return file_path

    @staticmethod
    def export_users_csv():

        ExportService.ensure_folder()

        file_path = (
            f"{ExportService.OUTPUT_FOLDER}/"
            f"users.csv"
        )

        users = User.query.all()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "ID",
                "Name",
                "Email",
                "Role",
                "Active"
            ])

            for user in users:

                writer.writerow([
                    user.id,
                    user.name,
                    user.email,
                    user.role,
                    user.active
                ])

        return file_path

    @staticmethod
    def export_submissions_csv():

        ExportService.ensure_folder()

        file_path = (
            f"{ExportService.OUTPUT_FOLDER}/"
            f"submissions.csv"
        )

        submissions = Submission.query.all()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "Reference",
                "Sample Number",
                "Customer",
                "Status",
                "Submitted At"
            ])

            for submission in submissions:

                writer.writerow([
                    submission.order_reference,
                    submission.sample_number,
                    submission.customer_name,
                    submission.status,
                    submission.submitted_at
                ])

        return file_path

    @staticmethod
    def export_audit_csv():

        ExportService.ensure_folder()

        file_path = (
            f"{ExportService.OUTPUT_FOLDER}/"
            f"audit.csv"
        )

        logs = AuditLog.query.all()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "Action",
                "User ID",
                "Object Type",
                "Object ID",
                "Created At"
            ])

            for log in logs:

                writer.writerow([
                    log.action,
                    log.user_id,
                    log.object_type,
                    log.object_id,
                    log.created_at
                ])

        return file_path

    @staticmethod
    def export_settings_json():

        ExportService.ensure_folder()

        file_path = (
            f"{ExportService.OUTPUT_FOLDER}/"
            f"settings.json"
        )

        settings = (
            SystemSettings.query.first()
        )

        if settings:

            data = {
                "company_name":
                settings.company_name,

                "smtp_server":
                settings.smtp_server,

                "smtp_port":
                settings.smtp_port,

                "smtp_sender_name":
                settings.smtp_sender_name,

                "smtp_sender_address":
                settings.smtp_sender_address
            }

        else:

            data = {}

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                default=str
            )

        return file_path

    @staticmethod
    def export_metrics_json():

        ExportService.ensure_folder()

        file_path = (
            f"{ExportService.OUTPUT_FOLDER}/"
            f"metrics.json"
        )

        data = {
            "status": "generated"
        }

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        return file_path

    @staticmethod
    def export_dropdowns_csv():

        ExportService.ensure_folder()

        file_path = (
            f"{ExportService.OUTPUT_FOLDER}/"
            f"dropdowns.csv"
        )

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "Category",
                "Value",
                "Description"
            ])

        return file_path

    @staticmethod
    def export_complete_system_zip():

        ExportService.ensure_folder()

        zip_file = (
            f"{ExportService.OUTPUT_FOLDER}/"
            f"system-export.zip"
        )

        export_files = [

            ExportService.export_customers_csv(),

            ExportService.export_users_csv(),

            ExportService.export_submissions_csv(),

            ExportService.export_audit_csv(),

            ExportService.export_settings_json(),

            ExportService.export_metrics_json(),

            ExportService.export_dropdowns_csv()

        ]

        with zipfile.ZipFile(
            zip_file,
            "w",
            zipfile.ZIP_DEFLATED
        ) as archive:

            for export_file in export_files:

                archive.write(
                    export_file,
                    Path(export_file).name
                )

        return zip_file