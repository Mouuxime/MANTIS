import unittest

from mantis.context import Context
from mantis.intent_parser import IntentParser
from mantis.nlg.templates import TemplatesNLG
from mantis.response import ResponseBuilder
from mantis.skill_router import SkillRouter
from mantis.skills.weather import WeatherSkill


class WeatherFlowTest(unittest.TestCase):
    def setUp(self):
        self.context = Context()
        self.parser = IntentParser()
        self.router = SkillRouter([WeatherSkill()])
        self.response_builder = ResponseBuilder()
        self.nlg = TemplatesNLG()

    def test_weather_flow_from_text_to_sentence(self):
        intent = self.parser.parse("meteo a Paris")

        self.assertIsNotNone(intent)

        skill = self.router.route(intent, self.context)

        self.assertIsInstance(skill, WeatherSkill)

        result = skill.execute(intent, self.context)
        response = self.response_builder.build(intent, result)
        text = self.nlg.generate(response=response)

        self.assertIn("paris", text)
        self.assertIn("20", text)
        self.assertIn("sunny", text)


if __name__ == "__main__":
    unittest.main()