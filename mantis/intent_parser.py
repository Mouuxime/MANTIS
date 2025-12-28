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
        
        if text in ("shutdown"):
            return Intent(
                name="system.shutdown",
                raw=text,
                source="cli",
                confidence=1.0
            )

        if any(word in text for word in ("météo", "meteo", "temps", "weather")):
            location = None

            for preposition in (" à ", " sur ", " pour "):
                if preposition in text:
                    location = text.split(preposition, 1)[1].strip()
                    break
            
            return Intent(
                name="weather.current",
                raw=text,
                source="cli",
                confidence=0.7,
                entities={"location": location} if location else {}
            )

        return None
