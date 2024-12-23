import random

from src.domain.character.base_schema import Character
from src.domain.schemas import ResultsDTO, SkillResult
from src.domain.skills.interface import ISkill
from src.utils import text


class BladeStrikeSkill(ISkill):
    name = 'удар клинком'
    skill_type = 'damage'
    damage_type = 'strength'
    using_count = 0
    limit = 999
    cooldown = 0
    damage = 10

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
                   history: list,
                   round: int
                   ) -> SkillResult:

        damage = player.strength * 0.20  # проценты от силы
        enemy_hp = enemy.hp
        enemy_hp_effects = sorted(enemy.tempo_stats, key=lambda x: x['expired'])

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

            elif effect['operation'] == 'replace':
                enemy_hp = effect['value']

            enemy.hp = enemy_hp - damage

        texts = text.blade_strike_skill(
                              done=True,
                              player_name=player.name,
                              enemy_name=enemy.name,
                              player_short=player.short_texts,
                              enemy_short=enemy.short_texts)
        return SkillResult(status=True, player_text=texts['player'], enemy_text=texts['enemy'])

    async def reflection(self,
                         player: Character,
                         enemy: Character,
                         round: int,
                         history: list
                         ) -> str:
        pass
