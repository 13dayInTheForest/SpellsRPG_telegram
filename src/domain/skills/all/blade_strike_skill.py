import random

from src.domain.schemas import RoomsInfo, ResultsDTO
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

    async def move(self, player_id: str, room: RoomsInfo) -> ResultsDTO:
        if self.using_count >= self.limit:
            return ResultsDTO(status=False, text='Лимит использования превышен')

        if player_id == room.u1:
            player = room.u1_class
            enemy = room.u2_class
        else:
            player = room.u2_class
            enemy = room.u1_class

        damage = random.randint(0, 10)
        enemy.character.hp -= damage

        return ResultsDTO(status=True,
                           text=text.blade_strike_skill(
                               player_name=player.character.name,
                               enemy_name=enemy.character.name,
                               player_short=player.character.short_texts,
                               enemy_short=enemy.character.short_texts
                           ))

    async def reflection(self, player_id: str, room: RoomsInfo) -> str:
        pass
