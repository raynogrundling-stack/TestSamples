from extensions import db
from models.user import User
from models.system_settings import (
    SystemSettings
)
class SandboxService:
    @staticmethod
    def is_enabled():
        settings = (
            SystemSettings.query.first()
        )
        if not settings:
            return False
        return settings.sandbox_enabled
    @staticmethod
    def disable_sandbox():
        settings = (
            SystemSettings.query.first()
        )
        if not settings:
            return False
        User.query.delete()
        settings.setup_completed = False
        settings.sandbox_enabled = False
        settings.sandbox_pending_disable = False
        db.session.commit()
        return True