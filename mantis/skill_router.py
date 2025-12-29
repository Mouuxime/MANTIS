"""
MANTIS - Skill Router
"""

from typing import List
from mantis.skills.base import Skill
from mantis.intent import Intent


class SkillRouter:
    def __init__(self, skills):
        self.skills = skills

    def route(self, intent, context):
        for skill in self.skills:
            if skill.can_handle(intent, context):
                return skill
        return None
