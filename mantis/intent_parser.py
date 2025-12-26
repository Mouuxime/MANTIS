"""
MANTIS Intent Parser
Simple rule-based text to Intent parser
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

        return None
