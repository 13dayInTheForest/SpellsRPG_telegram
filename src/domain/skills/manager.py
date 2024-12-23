from typing import Optional

from .catalog import skills_catalog
from .interface import ISkill
from ..character.base_schema import Character
from ..schemas import ResultsDTO, RoundStatsResult
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
        player.current_choice_type = skill.skill_type
        player.status = 'waiting'
        await player.state.set_state(FightStates.waiting)

        return ResultsDTO(status=True, text=f'Вы выбрали *{spell}*')

    async def fight(self) -> RoundStatsResult:
        u1_main_text = u2_main_text = ''
        u1_self_stats = u2_self_stats = ''
        u1_enemy_stats = u2_enemy_stats = ''

        # Если игрок 1 не выбрал ничего, просто применить выбор 2 игрока
        if self.u1.current_choice is None:
            skill: Optional[ISkill] = skills_catalog.get(self.u2.current_choice, False)
            result = await skill.move(
                self.u1,
                self.u2,
                self.round,
                self.history
            )
            if result.last_hit:
                return RoundStatsResult(
                    u1_text=result.enemy_text,
                    u2_text=result.player_text
                )

            # После навыка 2 юзера, 1 идет как enemy (result.enemy_stats)
            u2_main_text += f'{result.player_text}'
            u2_self_stats += f'{result.player_stats}\n'
            u2_enemy_stats += f'{result.enemy_stats}\n'

            u1_main_text += f'{result.enemy_text}'
            u1_self_stats += f'{result.enemy_stats}\n'
            u1_enemy_stats += f'{result.player_stats}\n'

        # Если игрок 2 не выбрал ничего, просто применить выбор 1 игрока
        elif self.u1.current_choice is None:
            skill: Optional[ISkill] = skills_catalog.get(self.u2.current_choice, False)
            result = await skill.move(
                self.u1,
                self.u2,
                self.round,
                self.history
            )
            if result.last_hit:
                return RoundStatsResult(
                    u1_text=result.player_text,
                    u2_text=result.enemy_text
                )

            # После навыка 2 юзера, 1 идет как enemy (result.enemy_stats)
            u1_main_text += f'{result.player_text}'
            u1_self_stats += f'{result.player_stats}\n'
            u1_enemy_stats += f'{result.enemy_stats}\n'

            u2_main_text += f'{result.enemy_text}'
            u2_self_stats += f'{result.enemy_stats}\n'
            u2_enemy_stats += f'{result.player_stats}\n'

        # Если кто-нибудь выбрал защиту
        if 'defend' in (self.u1.current_choice_type, self.u2.current_choice_type):
            # Если обы выбрали защиту
            if self.u1.current_choice_type == 'defend' and self.u2.current_choice_type == 'defend':
                pass

        # --------------------------------- СБОРКА ТЕКСТОВ -------------------------------------
        u1_result_text = (f'{u1_main_text}\n\n '  # --------------------------------- Главный текст
                          f'Вы:\n{u1_self_stats if u1_self_stats != "" else ""}\n'  # ---- Личные эффекты 
                          f'{u1_enemy_stats if u1_enemy_stats != "" else ""}')  # --- Эффекты врага

        u2_result_text = (f'{u2_main_text}\n\n '  # --------------------------------- Главный текст
                          f'Вы:\n{u2_self_stats if u2_self_stats != "" else ""}\n'  # ---- Личные эффекты 
                          f'Противник:\n{u2_enemy_stats if u2_enemy_stats != "" else ""}')  # --- Эффекты врага

        # Сброс выбора способностей
        self.u1.current_choice = None
        self.u2.current_choice = None
        self.u1.current_choice_type = None
        self.u2.current_choice_type = None

        return RoundStatsResult(
            u1_text=u1_result_text,
            u2_text=u2_result_text
        )

