import asyncio
from typing import Optional

from src.domain.character.base_schema import Character
from src.domain.rooms.interface import IRoom
from src.domain.schemas import ResultsDTO
from src.domain.skills.manager import SkillManager


class PVPRoom(IRoom):
    def __init__(self,
                 u1: Character,
                 u2: Character,
                 ):
        self.u1 = u1
        self.u2 = u2

        self.round: int = 1  # Подсчет раундов
        self.moves_history: list[dict] = []  # история ходов, пример ниже
        self.timer: Optional[asyncio.Task] = None

    """
    moves_history: [
        {'user_id': str, 'move': str, 'self': ['-1 здоровье'], 'enemy': ['-18 силы', '-1 здоровья']}
    ]
    """
    async def move(self, player_id: str, move_text: str) -> ResultsDTO:
        pass


