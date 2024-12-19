from src.domain.rooms.interface import IRoom
from typing import Literal
from src.domain.schemas import ResultsDTO, RoomsInfo
from src.domain.classes import IClass


class PVPRoom(IRoom):
    def __init__(self,
                 u1: str,  # телеграм id 1 юзера
                 u2: str,  # телеграм id 2 юзера
                 u1_class: IClass,  # Игровой Класс 1 юзера, наследуемый от BaseClass
                 u2_class: IClass,  # Игровой Класс 2 юзера, наследуемый от BaseClass
                 u1_status: Literal['waiting', 'moving'] = 'moving',
                 u2_status: Literal['waiting', 'moving'] = 'waiting',
                 ):
        self.stats = RoomsInfo(
            u1=u1,
            u2=u2,
            u1_class=u1_class,
            u2_class=u2_class,
            u1_status=u1_status,
            u2_status=u2_status,
            u1_current_chose=None,
            u2_current_chose=None
        )

    """
    moves_history: [
        {user_id: str, move: str, self: ['-1 здоровье'], enemy: ['-18 силы', '-1 здоровья']}
    ]
    """

    async def move(self, player_id: str, move_text: str) -> ResultsDTO:
        if player_id not in (self.stats.u1, self.stats.u2):
            return ResultsDTO(status=False, message='Ошибка! Попытка залезть не в свою комнату!')
        user_class = self.stats.u1_class if player_id == self.stats.u1 else self.stats.u2_class

        # skill = await user_class.spell(move_text, self.stats)
        # if not skill.status:  # Если вернется ошибка False, послать ошибку дальше
        #     return skill


        # return await skill.move(player_id)
