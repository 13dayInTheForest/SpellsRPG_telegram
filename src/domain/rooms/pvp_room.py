from src.domain.character.base_schema import Character
from src.domain.rooms.interface import IRoom
from src.domain.schemas import ResultsDTO, RoomsInfo


class PVPRoom(IRoom):
    def __init__(self,
                 u1: Character,  # телеграм id 1 юзера
                 u2: Character,  # телеграм id 2 юзера
                 ):
        self.u1 = u1
        self.u2 = u2

        self.round: int = 0  # Подсчет раундов
        self.moves_history: list[dict] = []  # история ходов, пример ниже


    """
    moves_history: [
        {'user_id': str, 'move': str, 'self': ['-1 здоровье'], 'enemy': ['-18 силы', '-1 здоровья']}
    ]
    """

    async def move(self, player_id: str, move_text: str) -> ResultsDTO:
        if player_id not in (self.stats.u1, self.stats.u2):
            return ResultsDTO(status=False, message='Ошибка! Попытка залезть не в свою комнату!')



