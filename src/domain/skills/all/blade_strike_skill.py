import random

from src.domain.character.base_schema import Character
from src.domain.schemas import ResultsDTO
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
                    ) -> bool:

        return True

    async def move(self,
                   player: Character,
                   enemy: Character,
                   history: list,
                   round: int
                   ):

        damage = player.strength * 0.20  # проценты от силы

        enemy_hp = int(enemy.hp)
        et_hp = 0
        for stat in enemy.tempo_stats.get('hp', []):
            if stat['operation'] == 'minus':
                et_hp -= stat['value']


            elif stat['operation'] == 'plus':
                et_hp += stat['value']
            elif stat['operation'] == 'replace':
                enemy_hp = stat['value']
                et_hp = 0
                break

        enemy.hp = enemy_hp + et_hp
