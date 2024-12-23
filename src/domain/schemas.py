from pydantic import BaseModel
from typing import Literal


class ResultsDTO(BaseModel):
    status: bool
    text: str = None


class SkillResult(BaseModel):
    status: bool
    player_text: str
    enemy_text: str
