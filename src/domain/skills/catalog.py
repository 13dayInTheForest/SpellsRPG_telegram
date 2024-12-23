from typing import Dict, Type

from src.domain.skills.all.blade_strike_skill import BladeStrikeSkill
from src.domain.skills.interface import ISkill


skills_catalog = {
    'BladeStrike': BladeStrikeSkill()
}

