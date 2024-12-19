from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from .states import MenuStates

from src.game.fight.states import FightStates


router = Router()


@router.message(MenuStates.main_menu)
async def main_menu(message: Message, state: FSMContext):
    text = message.text.lower()


