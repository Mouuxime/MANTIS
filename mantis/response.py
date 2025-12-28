"""
MANTIS - Response 
"""

class Response:
    def __init__(self, 
        type: str, 
        data: dict | None = None,
        skill: str | None = None,
        intent: str | None = None,
    ):
        self.type = type
        self.skill = skill
        self.intent = intent
        self.data = data or {}

    def __repr__(self):
        return (
            f"Response(type={self.type}, skill={self.skill}, "
            f"intent={self.intent}, data={self.data})"
        )

class ResponseBuilder:
    def build(self, intent, result) -> Response:
       if result is None:
           return Response(type="none")
       
       skill_name = intent.name.split(".", 1)[0]

       return Response(
           type="skill",
           skill=skill_name,
           intent=intent.name,
           data=result
       )