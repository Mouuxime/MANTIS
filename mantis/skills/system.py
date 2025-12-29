"""
System Skill
"""

from mantis.skills.base import Skill
from mantis.skills.registry import register
from mantis.permissions import SkillPermission
from mantis.intent import Intent

@register
class SystemSkill(Skill):
    name = "system.status"

    def can_handle(self, intent: str, context) -> bool:
        return intent.name == self.name

    def execute(self, intent: str, context):
        return {
            "status": context.get("system.status"),
            "user": context.get("user"),
        }
    
@register
class ExitSkill(Skill):
    name = "system.exit"
    permission = SkillPermission.SYSTEM
    allow_override = True

    def can_handle(self, intent: Intent, context) -> bool:
        return intent.name == self.name
    
    def execute(self, intent, context):
        self.kernel.logger.info("[FLOW] Exit requested")
        self.kernel.stop()
        return None

@register
class RestartSkill(Skill):
    name = "system.restart"
    permission = SkillPermission.ADMIN
    allow_override = True

    def can_handle(self, intent: Intent, context) -> bool:
        return intent.name == self.name
    
    def execute(self, intent, context):
        self.kernel.logger.info("[FLOW] Restart requested")
        self.kernel.restart(reason="intent:system.restart")
        return {"message": "Mantis is restarting."}

@register
class ShutdownSkill(Skill):
    name = "system.shutdown"
    permission = SkillPermission.ADMIN
    allow_override = True

    def can_handle(self, intent: Intent, context) -> bool:
        return intent.name == self.name
    
    def execute(self, intent, context):
        self.kernel.logger.info("[FLOW] Shutdown requested")
        self.kernel.shutdown(reason="intent:system.shutdown")
        return {"message": "Mantis is shutting down."}