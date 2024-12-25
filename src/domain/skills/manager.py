from typing import Optional

from .all.do_nothing import DoNothing
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

    @staticmethod
    async def choose(
            telegram_id: str,
            u1: Character,
            u2: Character,
            spell: str,
            history: list,
            round: int) -> ResultsDTO:

        if telegram_id == u1.telegram_id:
            player, enemy = u1, u2
        else:
            player, enemy = u2, u1

        #  Взять dev имя скила если он есть в Character, если его нет то вернуть False
        spell_dev_name = player.skills.get(spell.lower(), False)
        if not spell_dev_name:
            return ResultsDTO(status=False, text='У вас нет этого навыка')

        #  Найти класс скила по dev имени через каталог, если нет то вернуть False
        skill: Optional[ISkill] = skills_catalog.get(spell_dev_name, False)
        if not skill:
            return ResultsDTO(status=False, text='В данный момент этот навык не доступен в игре >:(')

        check_result = await skill.check(player=player, enemy=enemy, history=history, round=round)
        if not check_result.status:
            return ResultsDTO(status=False, text=check_result.text)

        player.current_choice = spell_dev_name
        player.current_choice_type = skill.skill_type
        player.status = 'waiting'
        await player.state.set_state(FightStates.waiting)

        return ResultsDTO(status=True, text=f'Вы выбрали *{spell}*')

    async def fight(self) -> RoundStatsResult:
        u1_text = {'main': '', 'stats': []}
        u2_text = {'main': '', 'stats': []}

        # Если 1 юзер выбрал защиту
        if 'defend' == self.u1.current_choice_type:
            u2_result = await self.__do_skill(2, u1=u1_text, u2=u2_text, reflected=True)
            if u2_result is not None:
                return u2_result

            u1_result = await self.__do_skill(1, u1=u1_text, u2=u2_text)
            if u1_result is not None:
                return u1_result

        # Если 2 юзер выбрал защиту
        elif 'defend' == self.u2.current_choice_type:
            u1_result = await self.__do_skill(1, u1=u1_text, u2=u2_text, reflected=True)
            if u1_result is not None:
                return u1_result

            u2_result = await self.__do_skill(2, u1=u1_text, u2=u2_text)
            if u2_result is not None:
                return u2_result

        # Если оба выбрали защиту
        elif 'defend' == self.u1.current_choice_type and 'defend' == self.u2.current_choice_type:
            u1_result = await self.__do_skill(1, u1=u1_text, u2=u2_text, reflected=True)
            if u1_result is not None:
                return u1_result

            u2_result = await self.__do_skill(2, u1=u1_text, u2=u2_text, reflected=True)
            if u2_result is not None:
                return u2_result

        # В случае если оба выбрали что-то кроме защиты
        else:
            if self.round % 2 != 0:  # Если раунд не четный, первым ходит юзер 1
                """ 1 юзер ходит первым """
                u1_result = await self.__do_skill(1, u1=u1_text, u2=u2_text)
                if u1_result is not None:
                    return u1_result

                u2_result = await self.__do_skill(2, u1=u1_text, u2=u2_text)
                if u2_result is not None:
                    return u2_result

            else:
                """ 2 юзер ходит первым """
                u2_result = await self.__do_skill(2, u1=u1_text, u2=u2_text)
                if u2_result is not None:
                    return u2_result

                u1_result = await self.__do_skill(1, u1=u1_text, u2=u2_text)
                if u1_result is not None:
                    return u1_result

        # --------------------------------- СБОРКА ТЕКСТОВ -------------------------------------
        u1_final_text = u1_text.get('main', '') + '\n'
        u2_final_text = u2_text.get('main', '') + '\n'

        if len(u1_text.get('stats')) > 0:
            u1_final_text += '\nТы:'
            for text in u1_text.get('stats'):
                u1_final_text += f'\n{text}'
        if len(u2_text.get('stats')) > 0:
            u1_final_text += '\nВраг:'
            for text in u2_text.get('stats'):
                u1_final_text += f'\n{text}'

        if len(u2_text.get('stats')) > 0:
            u2_final_text += '\nТы:'
            for text in u2_text.get('stats'):
                u2_final_text += f'\n{text}'
        if len(u1_text.get('stats')) > 0:
            u2_final_text += '\nВраг:'
            for text in u1_text.get('stats'):
                u2_final_text += f'\n{text}'

        # Сброс выбора способностей
        self.u1.current_choice = None
        self.u2.current_choice = None
        self.u1.current_choice_type = None
        self.u2.current_choice_type = None

        return RoundStatsResult(
            u1_text=u1_final_text,
            u2_text=u2_final_text
        )

    async def __do_skill(self,
                         user: 1 | 2,
                         u1: dict[str, list[str]],
                         u2: dict[str, list[str]],
                         reflected: bool = False
                         ) -> RoundStatsResult | None:
        """ Если кто-нибудь даст ласт хит, то метод вернет RoundStatsResult """
        if user == 1:
            u1_skill: Optional[ISkill] = skills_catalog.get(self.u1.current_choice, DoNothing)

            if reflected:  # Если удар отражен
                u1_result = await u1_skill.reflected(
                    player=self.u1,
                    enemy=self.u2,
                    round=self.round,
                    history=self.history
                )
            else:  # Обычное применение
                u1_result = await u1_skill.move(
                    player=self.u1,
                    enemy=self.u2,
                    round=self.round,
                    history=self.history
                )

            if u1_result.last_hit:  # Если после этого скила противник лишился всего хп
                return RoundStatsResult(
                    u1_text=u1_result.player_text,
                    u2_text=u1_result.enemy_text,
                    last_hit=self.u1.telegram_id
                )
            # Распаковка текстов после навыка
            u1['main'] += f'{u1_result.player_text}\n'
            u1['stats'].extend(u1_result.player_stats)
            u2['main'] += f'{u1_result.enemy_text}\n'
            u2['stats'].extend(u1_result.enemy_stats)

        elif user == 2:
            u2_skill: Optional[ISkill] = skills_catalog.get(self.u2.current_choice, DoNothing)
            if reflected:  # Если удар отражен
                u2_result = await u2_skill.reflected(
                    player=self.u2,
                    enemy=self.u1,
                    round=self.round,
                    history=self.history
                )
            else:  # Обычное применение
                u2_result = await u2_skill.move(
                    player=self.u2,
                    enemy=self.u1,
                    round=self.round,
                    history=self.history
                )

            if u2_result.last_hit:  # Если после этого скила противник лишился всего хп
                return RoundStatsResult(
                    u1_text=u2_result.enemy_text,
                    u2_text=u2_result.player_text,
                    last_hit=self.u1.telegram_id
                )
            # Распаковка текстов после навыка
            u2['main'] += f'{u2_result.player_text}\n'
            u2['stats'].extend(u2_result.player_stats)
            u1['main'] += f'{u2_result.enemy_text}\n'
            u1['stats'].extend(u2_result.enemy_stats)

        else:
            raise Exception(f'{__name__} В {self.__do_skill.__name__} можно указывать только 1 или 2')
