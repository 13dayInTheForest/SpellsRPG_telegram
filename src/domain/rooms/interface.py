import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Awaitable

from src.domain.character.base_schema import Character
from src.domain.schemas import ResultsDTO


class IRoom(ABC):
    u1: Character
    u2: Character

    round: int = 0  # Подсчет раундов
    moves_history: list[dict] = []  # история ходов, пример ниже

    @abstractmethod
    async def move(self, player_id: str, move_text: str) -> ResultsDTO:
        pass

