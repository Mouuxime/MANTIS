"""
Weather Skill
"""

from mantis.skills.base import Skill
from mantis.intent import Intent


class WeatherSkill(Skill):
    name = "weather"

    def can_handle(self, intent: Intent, context) -> bool:
        return intent.name in (
            "weather.current",
            "weather.now",
        )

    def execute(self, intent: Intent, context):
        # Placeholder weather data (V1)
        location = intent.data.get("location", "unknown") if intent.data else "unknown"

        return {
            "type": "skill",
            "skill": self.name,
            "intent": intent.name,
            "data": {
                "location": location,
                "temperature": 20,
                "condition": "sunny",
                "source": "mock",
            }
        }
