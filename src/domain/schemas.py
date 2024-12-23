from pydantic import BaseModel
from typing import Literal


class ResultsDTO(BaseModel):
    status: bool
    text: str = None


class SkillResult(BaseModel):
    status: bool
    player_text: str
    enemy_text: str
    player_stats: str = ''
    enemy_stats: str = ''
    last_hit: bool = False


class RoundStatsResult(BaseModel):
    u1_text: str
    u2_text: str
