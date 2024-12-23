from abc import ABC, abstractmethod
from typing import Literal

from src.domain.character.base_schema import Character
from src.domain.schemas import ResultsDTO, SkillResult


class ISkill(ABC):
    stats: dict
    skill_type: Literal['attack', 'defend', 'heal', 'buff', 'debuff']

    @abstractmethod
    async def check(self,
                    player: Character,
                    enemy: Character,
                    history: list,
                    round: int
                    ) -> ResultsDTO: ...

    @abstractmethod
    async def move(self,
                   player: Character,
                   enemy: Character,
                   round: int,
                   history: list
                   ) -> SkillResult: ...

    @abstractmethod
    async def reflection(self,
                         player: Character,
                         enemy: Character,
                         round: int,
                         history: list
                         ) -> SkillResult: ...

