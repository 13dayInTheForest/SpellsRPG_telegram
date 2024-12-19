from .base import BaseClass
from src.domain.classes import IClass

class Adventurer(BaseClass, IClass):
    skills = {
        'Удар клинком':
    }
    can_reflect = True



