from .base_schema import Character
from src.domain.skills.interface import ISkill
from src.domain.schemas import ResultsDTO, RoomsInfo
from src.utils import text


class BaseClass:
    character: Character
    skills: dict[str, ISkill]
    can_reflect: False

    def __init__(self, character: Character, add_skills: dict[str, ISkill] = None):
        self.character = character
        if add_skills:
            self.skills.update(add_skills)

    async def spell(self, telegram_id: str, skill_name: str, room_stat: RoomsInfo) -> ResultsDTO:
        skill = self.skills.get(skill_name)
        if skill is None:
            return ResultsDTO(status=False, message=text.dont_know_this_spell)

        skill_result = await skill.move(telegram_id, room_stat)

