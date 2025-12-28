from typing import Type, List
from mantis.skills.base import Skill

SKILL_REGISTRY: List[Type[Skill]] = []


def register(skill_cls: Type[Skill]) -> Type[Skill]:
    if not issubclass(skill_cls, Skill):
        raise TypeError("Only Skill subclasses can be registered")
    SKILL_REGISTRY.append(skill_cls)
    return skill_cls
