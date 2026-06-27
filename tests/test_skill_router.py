import unittest

from mantis.context import Context
from mantis.intent import Intent
from mantis.skill_router import SkillRouter
from mantis.skills.system import SystemSkill
from mantis.skills.weather import WeatherSkill


class SkillRouterTest(unittest.TestCase):
    def setUp(self):
        self.context = Context()
        self.router = SkillRouter([
            SystemSkill(),
            WeatherSkill(),
        ])

    def test_routes_system_status(self):
        intent = Intent(name="system.status", raw="status")

        skill = self.router.route(intent, self.context)

        self.assertIsInstance(skill, SystemSkill)

    def test_routes_weather_current(self):
        intent = Intent(name="weather.current", raw="meteo a Paris")

        skill = self.router.route(intent, self.context)

        self.assertIsInstance(skill, WeatherSkill)

    def test_returns_none_for_unknown_intent(self):
        intent = Intent(name="unknown", raw="hello")

        skill = self.router.route(intent, self.context)

        self.assertIsNone(skill)


if __name__ == "__main__":
    unittest.main()