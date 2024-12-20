from .catalog import skills_catalog
from ..character.base_schema import Character


class SkillManager:

    async def check(self,
                    spell: str,
                    character: Character,
                    enemy: Character,
                    history: list,
                    ) -> bool:

        #  Взять dev имя скила если он есть в Character, если его нет то вернуть False
        spell_dev_name = character.skills.get(spell.lower(), False)
        if not spell_dev_name:
            return False

        #  Найти класс скила по dev имени через каталог, если нет то вернуть False
        skill = skills_catalog.get(spell_dev_name, False)
        if not skill:
            return False

        return await skill.check

    async def move(self):
        """ Принимает только инты """
        tempo_fields = None
        if

        if len(character.tempo_stats) > 0:
            for stat in character.tempo_stats.get(field, []):
                if stat['operation'] == 'minus':
                    tempo_fields -= stat['value']

                elif stat['operation'] == 'plus':
                    tempo_fields += stat['value']


        return tempo_fields

