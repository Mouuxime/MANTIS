"""
MANTIS Skill Base
"""

from abc import ABC, abstractmethod
from mantis.intent import Intent
from mantis.permissions import SkillPermission

class Skill(ABC):
    name: str = "unnamed"
    permission: SkillPermission = SkillPermission.PUBLIC
    allow_override: bool = False

    @abstractmethod
    def can_handle(self, intent: str, context) -> bool:
        pass

    @abstractmethod
    def execute(self, intent: str, context):
        pass
