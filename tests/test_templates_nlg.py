import unittest

from mantis.nlg.templates import TemplatesNLG
from mantis.response import Response


class TemplatesNLGTest(unittest.TestCase):
    def setUp(self):
        self.nlg = TemplatesNLG()

    def test_generates_message_response_directly(self):
        response = Response(
            type="skill",
            skill="system",
            intent="system.override",
            data={"message": "Mode ADMIN activé pour : 5 minutes"},
        )

        text = self.nlg.generate(response=response)

        self.assertEqual(text, "Mode ADMIN activé pour : 5 minutes")

    def test_generates_system_status_response(self):
        response = Response(
            type="skill",
            skill="system",
            intent="system.status",
            data={
                "status": "running",
                "user": "Maxime",
            },
        )

        text = self.nlg.generate(response=response)

        self.assertIn("Maxime", text)

    def test_generates_weather_response(self):
        response = Response(
            type="skill",
            skill="weather",
            intent="weather.current",
            data={
                "location": "paris",
                "temperature": 20,
                "condition": "sunny",
            },
        )

        text = self.nlg.generate(response=response)

        self.assertIn("paris", text)
        self.assertIn("20", text)
        self.assertIn("sunny", text)

    def test_generates_weather_missing_location_prompt(self):
        response = Response(
            type="skill",
            skill="weather",
            intent="weather.current",
            data={
                "location": "unknown",
                "temperature": 20,
                "condition": "sunny",
            },
        )

        text = self.nlg.generate(response=response)

        self.assertIn("ville", text)


if __name__ == "__main__":
    unittest.main()