import unittest

from mantis.intent_parser import IntentParser


class IntentParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = IntentParser()

    def test_exact_system_commands(self):
        self.assertEqual(self.parser.parse("status").name, "system.status")
        self.assertEqual(self.parser.parse("restart").name, "system.restart")
        self.assertEqual(self.parser.parse("shutdown").name, "system.shutdown")
        self.assertEqual(self.parser.parse("sudo").name, "system.override")

    def test_partial_command_does_not_match(self):
        self.assertIsNone(self.parser.parse("r"))
        self.assertIsNone(self.parser.parse("start"))
        self.assertIsNone(self.parser.parse("shut"))

    def test_weather_location_extraction(self):
        intent = self.parser.parse("meteo a Paris")

        self.assertIsNotNone(intent)
        self.assertEqual(intent.name, "weather.current")
        self.assertEqual(intent.entities["location"], "paris")

    def test_weather_location_with_accent(self):
        intent = self.parser.parse("météo à Paris")

        self.assertIsNotNone(intent)
        self.assertEqual(intent.name, "weather.current")
        self.assertEqual(intent.entities["location"], "paris")

    def test_weather_location_english(self):
        intent = self.parser.parse("weather for London")

        self.assertIsNotNone(intent)
        self.assertEqual(intent.name, "weather.current")
        self.assertEqual(intent.entities["location"], "london")


if __name__ == "__main__":
    unittest.main()