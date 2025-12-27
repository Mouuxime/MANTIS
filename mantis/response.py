"""
MANTIS - Response 
"""

class Response:
    """
    A structured response describing what Mantis wants to communicate.
    The actual phrasing is handled by the NLG layer.
    """

    def __init__(self, type: str, data: dict | None = None):
        self.type = type
        self.data = data or {}

    def __repr__(self):
        return f"Response(type={self.type}, data={self.data})"


class ResponseBuilder:
    """
    Build structured responses from intents and skill results.
    """

    def build(self, intent, result) -> Response:
        """
        Convert an intent + skill result into a Response object.
        """

        if intent.name == "system.status":
            return Response(
                type="system_status",
                data={
                    "status": result.get("status"),
                    "user": result.get("user"),
                }
            )

        # Fallback generic response
        return Response(
            type="generic",
            data=result or {}
        )