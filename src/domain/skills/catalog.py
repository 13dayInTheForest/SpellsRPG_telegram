from typing import Dict, Type

from src.domain.skills.all.blade_strike_skill import BladeStrikeSkill
from src.domain.skills.all.do_nothing import DoNothing
from src.domain.skills.all.reflect_skill import ReflectSkill
from src.domain.skills.interface import ISkill


skills_catalog = {
    None: DoNothing(),
    'BladeStrike': BladeStrikeSkill(),
    'ReflectSkill': ReflectSkill(),
    'BloodyRevenge': None
}

