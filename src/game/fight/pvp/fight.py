import asyncio

from aiogram import Router, F
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.game.fight.states import FightStates
from src.game.menu.states import MenuStates
from src.main_env import waiting_users, storage, pvp_rooms
from src.infrastructure.bot import bot

from src.domain.rooms.pvp_room import PVPRoom
from src.domain.classes.adventurer import Adventurer
from src.domain.classes.base_schema import Character


router = Router()


@router.message(MenuStates.main_menu, F.text.lower() == 'бой')
async def fight_start(message: Message, state: FSMContext):
    """  Начало PVP боя  """
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

            user_1_id = str(message.from_user.id)
            user_2_id = str(waiting_users[0])

            await bot.send_message(waiting_users[0], text='бой найден, можете поговорить с противником')
            room = PVPRoom(
                u1=user_1_id,
                u2=user_2_id,
                u1_class=Adventurer(Character()),
                u2_class=Adventurer(Character()),
                u1_status='waiting',
                u2_status='waiting'
            )

            room_id = f'{user_1_id}_{user_2_id}'

            pvp_rooms[room_id] = room

            await message.answer('бой найден, можете поговорить с противником')
            await state.set_state(FightStates.conversation)
            await state2.set_state(FightStates.conversation)
            await state.update_data(room=room_id)
            await state2.update_data(room=room_id)

            await asyncio.sleep(15)
            await state.set_state(FightStates.move)
            await state2.set_state(FightStates.waiting)
            await message.answer('время разговоров окончено')
            await bot.send_message(user_2_id, 'время разговоров окончено')


@router.message(FightStates.starting)
async def wait(message: Message, state: FSMContext):
    if message.text == 'стоп':
        await state.set_state(MenuStates.main_menu)
        await message.answer('Вы вышли из очереди')
    else:
        await message.delete()
        mes = await message.answer('Имей терпение...')
        await asyncio.sleep(2)
        await mes.delete()


@router.message(FightStates.conversation)
async def conversation(message: Message, state: FSMContext):
    data = await state.get_data()
    room = pvp_rooms[data.get('room')]

    if message.from_user.id != room.stats.u1:
        await bot.send_message(room.stats.u1, message.text)
    else:
        await bot.send_message(room.stats.u2, message.text)


# --------------------------------------------------------------------------------------------


@router.message(FightStates.move)
async def fight(message: Message, state: FSMContext):
    pass


