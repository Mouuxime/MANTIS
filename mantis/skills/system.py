"""
System Skill
"""

from mantis.skills.base import Skill
from mantis.skills.registry import register
from mantis.intent import Intent

@register
class SystemSkill(Skill):
    name = "system"

    def can_handle(self, intent: str, context) -> bool:
        return intent.name == "system.status"

    def execute(self, intent: str, context):
        return {
            "status": context.get("system.status"),
            "user": context.get("user"),
        }
