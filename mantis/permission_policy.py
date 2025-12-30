from dataclasses import dataclass

@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    reason: str
    override_possible: bool = False

class PermissionPolicy:
    def check(self, user_permission, skill_permission, context=None) -> PermissionDecision:
        # Rule : User level >= skill level
        if user_permission.value >= skill_permission.value:
            return PermissionDecision(
                allowed=True,
                reason="permission_granted",
            )
        
        return PermissionDecision(
            allowed=False,
            reason="insufficient_permission",
            override_possible=True,
        )