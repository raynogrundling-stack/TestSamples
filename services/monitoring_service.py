from datetime import datetime
from pathlib import Path
import socket
import ssl
import time

from sqlalchemy import text

from extensions import db

from models.system_health import SystemHealth
from models.service_uptime import ServiceUptime
from models.backup_job import BackupJob
from models.restore_job import RestoreJob
from models.email_queue import EmailQueue

from services.logger import logger


APPLICATION_START_TIME = datetime.utcnow()


class MonitoringService:

    @staticmethod
    def record_health_check(
        component,
        status,
        message=None,
        response_time_ms=None
    ):

        record = SystemHealth(

            component=component,

            status=status,

            message=message,

            response_time_ms=response_time_ms,

            checked_at=datetime.utcnow()

        )

        db.session.add(record)

        db.session.commit()

        return record

    @staticmethod
    def record_service_uptime(
        service_name,
        status,
        response_time_ms=None
    ):

        record = ServiceUptime(

            service_name=service_name,

            status=status,

            response_time_ms=response_time_ms,

            checked_at=datetime.utcnow()

        )

        db.session.add(record)

        db.session.commit()

        return record

    @staticmethod
    def check_database():

        start = time.time()

        try:

            db.session.execute(
                text("SELECT 1")
            )

            duration = int(
                (time.time() - start)
                * 1000
            )

            return {

                "healthy": True,

                "response_time_ms":
                duration

            }

        except Exception as ex:

            logger.exception(
                "Database health check failed"
            )

            return {

                "healthy": False,

                "error": str(ex)

            }

    @staticmethod
    def check_backup_health():

        latest = (

            BackupJob.query

            .order_by(
                BackupJob.created_at.desc()
            )

            .first()

        )

        if not latest:

            return {

                "healthy": False,

                "reason":
                "No backups found"

            }

        return {

            "healthy":
            latest.status == "COMPLETED",

            "status":
            latest.status,

            "created_at":
            latest.created_at

        }

    @staticmethod
    def check_restore_health():

        latest = (

            RestoreJob.query

            .order_by(
                RestoreJob.created_at.desc()
            )

            .first()

        )

        if not latest:

            return {

                "healthy": True,

                "reason":
                "No restores executed"

            }

        return {

            "healthy":
            latest.status != "FAILED",

            "status":
            latest.status

        }

    @staticmethod
    def email_queue_health():

        pending = (

            EmailQueue.query

            .filter_by(
                status="PENDING"
            )

            .count()

        )

        retrying = (

            EmailQueue.query

            .filter_by(
                status="RETRYING"
            )

            .count()

        )

        failed = (

            EmailQueue.query

            .filter_by(
                status="FAILED"
            )

            .count()

        )

        return {

            "healthy":
            failed == 0,

            "pending":
            pending,

            "retrying":
            retrying,

            "failed":
            failed

        }

    @staticmethod
    def get_backup_health():

        return (
            MonitoringService
            .check_backup_health()
        )

    @staticmethod
    def get_restore_health():

        return (
            MonitoringService
            .check_restore_health()
        )

    @staticmethod
    def get_application_uptime():

        now = datetime.utcnow()

        return int(

            (
                now -
                APPLICATION_START_TIME
            ).total_seconds()

        )

    @staticmethod
    def get_system_summary():

        return {

            "database":

                MonitoringService
                .check_database(),

            "backup":

                MonitoringService
                .get_backup_health(),

            "restore":

                MonitoringService
                .get_restore_health(),

            "email":

                MonitoringService
                .email_queue_health()

        }

    @staticmethod
    def get_ssl_status(
        hostname=None,
        port=443
    ):

        if not hostname:

            return {

                "healthy": True,

                "message":
                "Hostname not configured"

            }

        try:

            context = (
                ssl.create_default_context()
            )

            with context.wrap_socket(

                socket.socket(),

                server_hostname=
                hostname

            ) as sock:

                sock.settimeout(5)

                sock.connect(
                    (hostname, port)
                )

                cert = (
                    sock.getpeercert()
                )

            expiry = cert.get(
                "notAfter"
            )

            return {

                "healthy": True,

                "expires": expiry

            }

        except Exception as ex:

            logger.exception(
                "SSL validation failed"
            )

            return {

                "healthy": False,

                "error": str(ex)

            }

    @staticmethod
    def backup_storage_usage(
        backup_path="/backups"
    ):

        path = Path(backup_path)

        if not path.exists():

            return {

                "exists": False,

                "size_bytes": 0

            }

        total_size = 0

        for item in path.glob(
            "**/*"
        ):

            if item.is_file():

                total_size += (
                    item.stat().st_size
                )

        return {

            "exists": True,

            "size_bytes":
            total_size

        }

    @staticmethod
    def collect_all_health_checks():

        summary = (
            MonitoringService
            .get_system_summary()
        )

        db_health = summary[
            "database"
        ]

        MonitoringService.record_health_check(

            component="DATABASE",

            status=(
                "HEALTHY"
                if db_health.get(
                    "healthy"
                )
                else "FAILED"
            ),

            response_time_ms=
            db_health.get(
                "response_time_ms"
            )

        )

        email_health = summary[
            "email"
        ]

        MonitoringService.record_health_check(

            component="EMAIL",

            status=(
                "HEALTHY"
                if email_health.get(
                    "healthy"
                )
                else "FAILED"
            )

        )

        backup_health = summary[
            "backup"
        ]

        MonitoringService.record_health_check(

            component="BACKUP",

            status=(
                "HEALTHY"
                if backup_health.get(
                    "healthy"
                )
                else "FAILED"
            )

        )

        restore_health = summary[
            "restore"
        ]

        MonitoringService.record_health_check(

            component="RESTORE",

            status=(
                "HEALTHY"
                if restore_health.get(
                    "healthy"
                )
                else "FAILED"
            )

        )

        return summary