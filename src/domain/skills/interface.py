from abc import ABC, abstractmethod
from typing import Literal

from src.domain.character.base_schema import Character
from src.domain.schemas import RoomsInfo


class ISkill(ABC):
    stats: dict
    skill_type: Literal['attack', 'defend', 'heal', 'buff', 'debuff']

    @abstractmethod
    async def move(self,
                   player: Character,
                   enemy: Character,
                   round: int,
                   history: list
                   ) -> str:
        pass

    @abstractmethod
    async def reflection(self, player_id: str, room: RoomsInfo) -> str:
        pass

