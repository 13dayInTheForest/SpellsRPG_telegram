from abc import ABC, abstractmethod
from typing import Literal

from src.domain.classes.base_schema import Character
from src.domain.schemas import RoomsInfo
from src.domain.skills.interface import ISkill


class IClass(ABC):
    character: Character
    skills: dict
    can_reflect: bool

    # @abstractmethod
    # async def spell(self, skill_name: str, room_stat: RoomsInfo) -> ResultsDTO:
    #     pass

