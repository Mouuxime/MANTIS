from enum import IntEnum

class SkillPermission(IntEnum):
    PUBLIC = 1
    SYSTEM = 2
    ADMIN = 3

class UserPermission(IntEnum):
    GUEST = 1
    USER = 2
    ADMIN = 3