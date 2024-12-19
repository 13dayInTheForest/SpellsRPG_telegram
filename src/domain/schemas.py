from pydantic import BaseModel
from typing import Literal
from src.domain.classes.interface import IClass


class ResultsDTO(BaseModel):
    status: bool
    text: str


class CharacterBattleInfo(BaseModel):
    id: str
    user_class: IClass  # Игровой Класс 1 юзера, наследуемый от BaseClass
    tempo_class: IClass
    tc_to_round: int = 0  # Tempo Class to Round \ До какого раунда пользоваться временным классом
    status: Literal['waiting', 'moving'] = 'waiting'
    passed: int = 0  # Сколько ходов пропустил юзер
    state = None


class RoomsInfo(BaseModel):
    u1: CharacterBattleInfo
    u2: CharacterBattleInfo

    round: int = 0  # Подсчет раундов
    moves_history: list[dict] = []  # история ходов, пример ниже

    u1_current_chose = None,
    u2_current_chose = None


class UpdateRoomsInfo(BaseModel):
    u1: str = None
    u1_class: IClass = None
    u1_tempo_class: IClass = None
    u1_ts_to_round: int = None
    u1_status: Literal['waiting', 'moving'] = None
    u1_passed: int = None

    u2: str = None
    u2_class: IClass = None
    u2_tempo_stats: IClass = None
    u2_ts_to_round: int = None
    u2_status: Literal['waiting', 'moving'] = None
    u2_passed: int = None

