from src.domain.character.base_schema import Character
from src.domain.schemas import ResultsDTO, SkillResult
from src.domain.skills.interface import ISkill


class DoNothing(ISkill):
    """ Навык-заглушка для бездействия """
    skill_type = 'nothing'

    async def check(self,
                    player: Character,
                    enemy: Character,
                    history: list,
                    round: int
                    ) -> ResultsDTO:
        return ResultsDTO(status=True)

    async def move(self,
                   player: Character,
                   enemy: Character,
                   round: int,
                   history: list
                   ) -> SkillResult:
        damage = 0

        for skill in history:
            pass

        enemy_hp_effects = sorted(enemy.tempo_stats.get('hp', {}), key=lambda x: x['expired'])

        for effect in enemy_hp_effects:
            if effect['value'] <= 0:
                continue

            elif effect['operation'] == 'plus':
                if effect['value'] < damage:
                    damage -= effect['value']
                    effect['value'] = 0
                    if damage <= 0:
                        break
                else:
                    effect['value'] -= damage
                    break

        enemy.hp -= damage

        if enemy.hp <= 0:
            last_hit = True

        else:
            last_hit = False

        return SkillResult(
            status=True,
            player_text='КРОВАВАЯ МЕЕЕЕСТЬ',
            enemy_text='КРОВАВАЯ МЕЕЕЕСТЬ'
        )

    async def reflected(self,
                        player: Character,
                        enemy: Character,
                        round: int,
                        history: list
                        ) -> SkillResult:

        return SkillResult(
            status=True,
            player_text='',
            enemy_text=''
        )
