import asyncio

from aiogram import Router, F
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.game.fight.states import FightStates
from src.game.menu.states import MenuStates
from src.main_env import waiting_users, pvp_rooms, storage
from src.infrastructure.bot import bot


router = Router()


@router.message(MenuStates.main_menu, F.text.lower() == 'бой')
async def fight_start(message: Message, state: FSMContext):
    """  Начало PVE боя  """
    await state.set_state(FightStates.starting)
    await message.answer('ищем бой')
    if len(waiting_users) < 1:
        waiting_users.append(message.from_user.id)
    else:
        if waiting_users[0] != message.from_user.id:
            state2 = FSMContext(storage, key=StorageKey(
                user_id=waiting_users[0],
                chat_id=waiting_users[0],
                bot_id=bot.id
            ))
            user2 = waiting_users[0]
            await bot.send_message(waiting_users[0], text='бой найден, можете поговорить с противником')
            pvp_rooms.extend([message.from_user.id, waiting_users[0]])
            waiting_users.clear()

            await message.answer('бой найден, можете поговорить с противником')
            await state.set_state(FightStates.conversation)
            await state2.set_state(FightStates.conversation)
            await asyncio.sleep(15)
            await state.set_state(FightStates.move)
            await state2.set_state(FightStates.waiting)
            await message.answer('время разговоров окончено')
            await bot.send_message(user2, 'время разговоров окончено')


@router.message(FightStates.starting)
async def wait(message: Message, state: FSMContext):
    if message.text == 'стоп':
        await state.set_state(MenuStates.main_menu)
        await message.answer('Вы вышли из очереди')
    else:
        await message.delete()
        mes = await message.answer('имей терпение')
        await asyncio.sleep(2)
        await mes.delete()


@router.message(FightStates.conversation)
async def conversation(message: Message):
    if message.from_user.id != pvp_rooms[0]:
        await bot.send_message(pvp_rooms[0], message.text)
    else:
        await bot.send_message(pvp_rooms[1], message.text)
