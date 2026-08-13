import os
import zipfile
from datetime import datetime
class BackupService:
    BACKUP_DIR = "backups"
    @staticmethod
    def create_backup():
        os.makedirs(
            BackupService.BACKUP_DIR,
            exist_ok=True
        )
        timestamp = datetime.utcnow().strftime(
            "%Y%m%d_%H%M%S"
        )
        filename = (
            f"backup_{timestamp}.zip"
        )
        filepath = os.path.join(
            BackupService.BACKUP_DIR,
            filename
        )
        with zipfile.ZipFile(
            filepath,
            "w",
            zipfile.ZIP_DEFLATED
        ) as backup_zip:
            for directory in [
                "uploads",
                "generated",
                "logs"
            ]:
                if not os.path.exists(
                    directory
                ):
                    continue
                for root, dirs, files in os.walk(
                    directory
                ):
                    for file in files:
                        full_path = os.path.join(
                            root,
                            file
                        )
                        backup_zip.write(
                            full_path
                        )
        return filepath
    @staticmethod
    def verify_backup(filepath):
        return os.path.exists(
            filepath
        )
    @staticmethod
    def delete_backup(filepath):
        if os.path.exists(
            filepath
        ):
            os.remove(filepath)
    @staticmethod
    def list_backups():
        os.makedirs(
            BackupService.BACKUP_DIR,
            exist_ok=True
        )
        return sorted(
            os.listdir(
                BackupService.BACKUP_DIR
            ),
            reverse=True
        )