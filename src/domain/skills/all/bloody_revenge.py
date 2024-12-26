from src.domain.character.base_schema import Character
from src.domain.schemas import ResultsDTO, SkillResult
from src.domain.skills.interface import ISkill


class BloodyRevenge(ISkill):
    """ Навык-заглушка для бездействия """
    skill_type = 'nothing'

    async def check(self,
                    player: Character,
                    enemy: Character,
                    history: list,
                    round: int
                    ) -> ResultsDTO:
        if player.hp < player.max_hp // 4:
            return ResultsDTO(status=False, text='Не достаточно здоровья для навыка')
        return ResultsDTO(status=True)

    async def move(self,
                   player: Character,
                   enemy: Character,
                   round: int,
                   history: list
                   ) -> SkillResult:
        """ Урон равен всему нанесенному урону от врага за всю историю комнаты """
        damage = 0
        self_damage = player.max_hp // 4
        for skill in history:
            if enemy.telegram_id == skill['user_id']:
                if skill['choice_type'] == 'damage':
                    for effects in skill.get('enemy', []):
                        if effects['operation'] == 'minus':
                            damage += effects['value']

        damage_for_stats = int(damage)
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

        player_hp_effects = sorted(player.tempo_stats.get('hp', {}), key=lambda x: x['expired'])

        for effect in player_hp_effects:
            if effect['value'] <= 0:
                continue

            elif effect['operation'] == 'plus':
                if effect['value'] < self_damage:
                    self_damage -= effect['value']
                    effect['value'] = 0
                    if self_damage <= 0:
                        break
                else:
                    effect['value'] -= self_damage
                    break

        if enemy.hp <= 0:
            last_hit = True

        else:
            last_hit = False

        player.choice_enemy_effects = ([{'field': 'hp', 'operation': 'minus', 'value': self_damage}])
        player.choice_self_effects = ([{'field': 'hp', 'operation': 'minus', 'value': damage_for_stats}])

        return SkillResult(
            status=True,
            player_text='КРОВАВАЯ МЕЕЕЕСТЬ',
            enemy_text='КРОВАВАЯ МЕЕЕЕСТЬ',
            player_stats=[f'-{self_damage} Здоровья'],
            enemy_stats=[f'-{damage_for_stats} Здоровья'],
            last_hit=last_hit
        )

    async def reflected(self,
                        player: Character,
                        enemy: Character,
                        round: int,
                        history: list
                        ) -> SkillResult:
        player_hp_effects = sorted(player.tempo_stats.get('hp', {}), key=lambda x: x['expired'])
        self_damage = player.max_hp // 4

        for effect in player_hp_effects:
            if effect['value'] <= 0:
                continue

            elif effect['operation'] == 'plus':
                if effect['value'] < self_damage:
                    self_damage -= effect['value']
                    effect['value'] = 0
                    if self_damage <= 0:
                        break
                else:
                    effect['value'] -= self_damage
                    break

        return SkillResult(
            status=True,
            player_text='КРОВАВАЯ МЕЕЕЕСТЬ, не удалась',
            enemy_text='КРОВАВАЯ МЕЕЕЕСТЬ, не удалась',
            player_stats=[f'-{self_damage} Здоровья'],
        )
