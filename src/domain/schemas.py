from pydantic import BaseModel
from typing import Literal

from src.domain.character.base_schema import Character


class ResultsDTO(BaseModel):
    status: bool
    text: str


class CharacterBattleInfo(BaseModel):
    id: str
    stats: Character  # Игровой Класс 1 юзера, наследуемый от BaseClass
    tempo_stats: Character | None = None
    ts_to_round: int = 0  # Tempo Stats to Round \ До какого раунда пользоваться временным классом
    status: Literal['waiting', 'moving'] = 'moving'
    passed: int = 0  # Сколько ходов пропустил юзер
    state: None = None
    u2_current_chose: None = None


class RoomsInfo(BaseModel):  # Убрать это --------------------------------------------------------------------------------
    u1: CharacterBattleInfo
    u2: CharacterBattleInfo

    round: int = 0  # Подсчет раундов
    moves_history: list[dict] = []  # история ходов, пример ниже



