import unittest

from mantis.intent import Intent
from mantis.response import ResponseBuilder


class ResponseBuilderTest(unittest.TestCase):
    def setUp(self):
        self.builder = ResponseBuilder()

    def test_builds_none_response(self):
        intent = Intent(name="system.exit", raw="exit")

        response = self.builder.build(intent, None)

        self.assertEqual(response.type, "none")
        self.assertEqual(response.data, {})

    def test_builds_skill_response_from_dict(self):
        intent = Intent(name="weather.current", raw="meteo a Paris")
        result = {
            "location": "paris",
            "temperature": 20,
        }

        response = self.builder.build(intent, result)

        self.assertEqual(response.type, "skill")
        self.assertEqual(response.skill, "weather")
        self.assertEqual(response.intent, "weather.current")
        self.assertEqual(response.data["location"], "paris")
        self.assertEqual(response.data["temperature"], 20)

    def test_builds_skill_response_from_string(self):
        intent = Intent(name="system.override", raw="sudo")
        result = "Mode ADMIN activé pour : 5 minutes"

        response = self.builder.build(intent, result)

        self.assertEqual(response.type, "skill")
        self.assertEqual(response.skill, "system")
        self.assertEqual(response.intent, "system.override")
        self.assertEqual(
            response.data,
            {"message": "Mode ADMIN activé pour : 5 minutes"},
        )


if __name__ == "__main__":
    unittest.main()