from src.domain.character.base_schema import Character
from src.domain.schemas import ResultsDTO, SkillResult
from src.domain.skills.interface import ISkill


class ReflectSkill(ISkill):
    skill_type = 'defend'
    min_hp = 20

    async def check(self,
                    player: Character,
                    enemy: Character,
                    history: list,
                    round: int
                    ) -> ResultsDTO:
        if player.hp >= self.min_hp:
            return ResultsDTO(status=False, text='Этот навык можно использовать только при хп ниже 20')
        return ResultsDTO(status=True)

    async def move(self,
                   player: Character,
                   enemy: Character,
                   round: int,
                   history: list
                   ) -> SkillResult:

        return SkillResult(
            status=True,
            player_text='Вы отразили весь урон',
            enemy_text='Враг отразил весь урон'
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
