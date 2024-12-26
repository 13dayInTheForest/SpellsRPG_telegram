from aiogram.fsm.context import FSMContext
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal


class Character(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Разрешить сторонние типы валидации, FSMContext

    skills: dict = {"удар клинком": "BladeStrike", 'кровавая месть': 'BloodyRevenge', 'полное отражение': 'ReflectSkill'}  # {"удар клинком": "BladeStrike"}
    class_dev_name: str = 'vic'
    state: FSMContext = None
    in_battle: bool = True

    tempo_stats: dict = {}  # ------ временные эффекты, пример ниже
    status: Literal['waiting', 'moving'] = 'moving'
    passed: int = 0  # Сколько ходов пропустил юзер
    current_choice: str | None = None  # dev имя скила
    current_choice_type: Literal['attack', 'defend', 'heal', 'buff', 'debuff'] | None = None  # тип выбранного навыка
    choice_self_effects: list | None = None  # Эффекты от своего навыка, только для документации
    choice_enemy_effects: list | None = None  # Эффекты от своего навыка, только для документации

    """
    tempo_stats: {
        "Поле": [{"value": Значение, "operation": Операция, "expired": Раунд завершения эффекта}]
        
        "hp": [{"value": 40, "operation": "plus", "expired": 7}],
        "strength": [{"value": 10, "operation": "minus", ""expired"": 3}],
        "can_fight": [{"value": False, "operation": "replace", "expired": 4}]
    }
    """

    id: str = '1223'
    telegram_id: str = '67821449'
    name: str = 'test'
    avatar_prompt: str = ''
    avatar_prompt_ru: str = ''
    avatar_url: str = ''
    hp: int = 100
    max_age: int = 70
    max_mana: int = 10
    max_hp: int = 100
    gold: int = 100
    karma: int = 10
    strength: int = 10
    mana: int = 10
    shield: int = 0
    max_shield: int = 0
    exp_points: int = 10
    title: Optional[str] = None
    type: str = 'player'
    reputation: int = 0
    armor: Optional[str] = None
    weapon: Optional[str] = None
    backpack_size: int = 10
    can_speak: bool = True
    can_hear: bool = True
    can_see: bool = True
    can_move: bool = True
    can_play: bool = True
    can_fight: bool = True
    can_defend: bool = True
    can_worship_gods: bool = True
    can_have_items: bool = True
    can_have_backpack: bool = True
    can_have_friends: bool = True
    can_kill_players: bool = True
    can_be_killed: bool = True
    can_be_seen: bool = True
    can_be_revived: bool = False
    can_be_cursed: bool = True
    can_be_healed: bool = True
    can_see_enemy_choose: bool = False
    class_id: Optional[str] = None
    potential_id: Optional[str] = None
    god_id: Optional[str] = None
    weakness_id: Optional[str] = None
    born_kingdom_id: Optional[int] = None
    citizen_kingdom_id: Optional[int] = None
    dungeon_cleared: int = 0
    monsters_killed: int = 0
    human_killed: int = 0
    friends_count: int = 0
    unlimited_mana: bool = False
    unlimited_karma: bool = False
    unlimited_strength: bool = False
    unlimited_shield: bool = False
    short_texts: bool = False
