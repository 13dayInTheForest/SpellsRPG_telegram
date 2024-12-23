from typing import Optional

from .catalog import skills_catalog
from .interface import ISkill
from ..character.base_schema import Character
from ..schemas import ResultsDTO
from ...game.fight.states import FightStates


class SkillManager:
    def __init__(self,
                 u1: Character,
                 u2: Character,
                 history: list,
                 round: int
                 ):
        self.u1 = u1
        self.u2 = u2
        self.history = history
        self.round = round

    async def choose(self, telegram_id: str, spell: str) -> ResultsDTO:
        if telegram_id == self.u1.telegram_id:
            player, enemy = self.u1, self.u2
        else:
            player, enemy = self.u2, self.u1

        #  Взять dev имя скила если он есть в Character, если его нет то вернуть False
        spell_dev_name = player.skills.get(spell.lower(), False)
        if not spell_dev_name:
            return ResultsDTO(status=False, text='У вас нет этого навыка')

        #  Найти класс скила по dev имени через каталог, если нет то вернуть False
        skill: Optional[ISkill] = skills_catalog.get(spell_dev_name, False)
        if not skill:
            return ResultsDTO(status=False, text='В данный момент этот навык не доступен в игре >:(')

        check_result = await skill.check(player=player, enemy=enemy, history=self.history, round=self.round)
        if not check_result.status:
            return check_result

        player.current_choice = spell_dev_name
        player.status = 'waiting'
        await player.state.set_state(FightStates.waiting)

        return ResultsDTO(status=True, text=f'Вы выбрали *{spell}*')

    async def move(self):

        # skill = skills_catalog.get(skill_dev_name)
        #
        # if telegram_id == self.
        #
        # result = skill.move(
        #
        # )
        pass


