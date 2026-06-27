"""
MANTIS - Intent Parser
"""

from mantis.intent import Intent

class IntentParser:
    def parse(self, text: str) -> Intent | None:
        raw = text
        command = text.strip().lower()

        if command in ("exit", "quit",):
            return Intent("system.exit", raw=raw, source="cli", confidence=1.0)
        
        if command in ("restart",):
            return Intent("system.restart", raw=raw, source="cli", confidence=1.0)
        
        if command in ("shutdown",):
            return Intent("system.shutdown", raw=raw, source="cli", confidence=1.0)
        
        if command in ("status", "system status", "system.status",):
            return Intent("system.status", raw=raw, source="cli", confidence=1.0)
        
        if command in ("sudo", "system.override",):
            return Intent("system.override", raw=raw, source="cli", confidence=1.0)
        

        if any(word in command for word in ("météo", "meteo", "temps", "weather")):
            location = None

            for preposition in (" à ", " a ", " sur ", " pour ", "for"):
                if preposition in command:
                    location = command.split(preposition, 1)[1].strip()
                    break
            
            return Intent(
                name="weather.current",
                raw=raw,
                source="cli",
                confidence=0.7,
                entities={"location": location} if location else {}
            )

        return None
