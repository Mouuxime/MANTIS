"""
Weather Skill
"""

from mantis.skills.base import Skill
from mantis.skills.registry import register
from mantis.permissions import SkillPermission
from mantis.intent import Intent

@register
class WeatherSkill(Skill):
    name = "weather"
    permission = SkillPermission.PUBLIC

    def can_handle(self, intent: Intent, context) -> bool:
        return intent.name in (
            "weather.current",
            "weather.now",
        )

    def execute(self, intent: Intent, context):
        # Placeholder weather data (V1)
        location = intent.entities.get("location", "unknown")

        return {
                "location": location,
                "temperature": 20,
                "condition": "sunny",
                "source": "mock",
        }
