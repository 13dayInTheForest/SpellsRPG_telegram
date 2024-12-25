import asyncio
from src.infrastructure.bot import bot

from aiogram.enums.parse_mode import ParseMode
from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

import src.infrastructure.keyboards.menu as kb
from src.infrastructure.database.gods import gods
from src.game.fight.pvp.fight import router as fight_router
from src.main_env import storage

from src.logging_config import setup_logging


dp = Dispatcher(storage=storage)
dp.include_router(fight_router)
setup_logging()


class MenuStates(StatesGroup):
    main_menu = State()

    shop_menu = State()
    gods = State()


class BattleStates(StatesGroup):
    starting = State()
    move = State()
    waiting_for_enemy = State()


@dp.message(Command('start'))
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(MenuStates.main_menu)
    await message.answer('С возвращением!', reply_markup=kb.main_menu_keyboard())


@dp.message(BattleStates.starting)
async def please_wait(message: Message):
    await message.answer('Прояви терпение...')


@dp.message(MenuStates.shop_menu)
async def shop_menu(message: Message, state: FSMContext):
    if message.text.lower() == 'контракты':
        await message.answer("Выбери бога себе по душе", reply_markup=ReplyKeyboardRemove())
        await message.answer(f'{gods.get("god_zeus")}', reply_markup=kb.gods_keyboard())
        await state.set_state(MenuStates.gods)
    else:
        print(await state.get_state())
        print(state.storage)
        await state.clear()


@dp.callback_query()
async def gods_handler(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    if callback.data in ('god_go_back', 'god_go_next'):
        await callback.answer('пока не доделав >:(')
    elif callback.data == 'god_go_exit':
        await callback.message.delete()
        await callback.message.answer('Вы вернулись в меню', reply_markup=kb.main_menu_keyboard())
        await state.set_state(MenuStates.main_menu)
    else:
        await callback.message.edit_text(f'{gods.get(callback.data)}', reply_markup=kb.gods_keyboard())
        await callback.answer()


async def main():
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())