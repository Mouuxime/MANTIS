"""
MANTIS - Intent Parser
"""

from mantis.intent import Intent


class IntentParser:
    def parse(self, text: str) -> Intent | None:
        text = text.strip().lower()

        if text in ("status", "system status", "system.status"):
            return Intent(
                name="system.status",
                raw=text,
                source="cli",
                confidence=1.0
            )

        if any(word in text for word in ("météo", "meteo", "temps", "weather")):
            return Intent(
                name="weather.current",
                raw=text,
                source="cli",
                confidence=0.7,
                entities={}
            )

        return None
