from abc import ABC, abstractmethod
from typing import Literal


class ISkill(ABC):
    stats: dict
    skill_type: Literal['attack', 'defend', 'other']

    @abstractmethod
    async def move(self, player_id: str, room: RoomsInfo) -> str:
        pass

    @abstractmethod
    async def reflection(self, player_id: str, room: RoomsInfo) -> str:
        pass

