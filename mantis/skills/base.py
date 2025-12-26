"""
MANTIS Skill Base
"""

from abc import ABC, abstractmethod
from mantis.intent import Intent


class Skill(ABC):
    name: str = "unnamed"

    @abstractmethod
    def can_handle(self, intent: str, context) -> bool:
        """
        Return True if this skill can handle the intent.
        """
        pass

    @abstractmethod
    def execute(self, intent: str, context):
        """
        Execute the skill.
        """
        pass
