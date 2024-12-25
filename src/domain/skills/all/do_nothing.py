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

        return SkillResult(
            status=True,
            player_text='Вы ничего не делаете...',
            enemy_text='Ваш враг стоит неподвижно.'
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
