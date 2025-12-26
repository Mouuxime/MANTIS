"""
MANTIS Skill Router
Routes intents to the appropriate skill.
"""

from typing import List
from mantis.skills.base import Skill
from mantis.intent import Intent


class SkillRouter:
    def __init__(self, skills: List[Skill]):
        self.skills = skills

    def route(self, intent: Intent, context):
        for skill in self.skills:
            if skill.can_handle(intent, context):
                return skill.execute(intent, context)
        return None
