import os
import zipfile


class RestoreService:

    @staticmethod
    def restore_backup(backup_file):

        if not os.path.exists(backup_file):

            raise FileNotFoundError(
                f"Backup not found: {backup_file}"
            )

        extract_dir = "restore_tmp"

        os.makedirs(
            extract_dir,
            exist_ok=True
        )

        with zipfile.ZipFile(
            backup_file,
            "r"
        ) as zip_ref:

            zip_ref.extractall(
                extract_dir
            )

        return True