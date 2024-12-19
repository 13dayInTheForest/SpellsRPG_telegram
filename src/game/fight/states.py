from aiogram.fsm.state import StatesGroup, State


class FightStates(StatesGroup):
    starting = State()
    conversation = State()
    move = State()
    waiting = State()
