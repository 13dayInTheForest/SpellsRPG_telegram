import asyncio

from aiogram import Router, F
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.domain.character.base_schema import Character
from src.domain.skills.manager import SkillManager
from src.game.fight.states import FightStates
from src.game.fight.utils import timer_task
from src.game.menu.states import MenuStates
from src.infrastructure.keyboards.battle import skills_buttons
from src.infrastructure.keyboards.menu import main_menu_keyboard
from src.main_env import waiting_users, storage, pvp_rooms
from src.infrastructure.bot import bot

from src.domain.rooms.pvp_room import PVPRoom

from logging import getLogger


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
                u1=Character(telegram_id=user_1_id, state=state),
                u2=Character(telegram_id=user_2_id, state=state2),
            )

            room_id = f'{user_1_id}_{user_2_id}'

            pvp_rooms[room_id] = room

            await message.answer('бой найден, можете поговорить с противником')
            await state.set_state(FightStates.conversation)
            await state2.set_state(FightStates.conversation)
            await state.update_data(room=room_id)
            await state2.update_data(room=room_id)

            manager = SkillManager(
                u1=room.u1,
                u2=room.u2,
                history=room.moves_history,
                round=room.round
            )

            # Время на разговор
            await asyncio.sleep(5)

            while room.u1.hp > 0 and room.u2.hp > 0:
                await state.set_state(FightStates.move)
                await state2.set_state(FightStates.move)

                await message.answer(f'Раунд {room.round} | 30 секунд')
                await bot.send_message(user_2_id, f'Раунд {room.round} | 30 секунд')

                await message.answer('Выберите действие', reply_markup=skills_buttons(['Удар клинком', 'Сдаться']))
                await bot.send_message(user_2_id, 'Выберите действие',
                                       reply_markup=skills_buttons(['Удар клинком', 'Сдаться']))

                timer = 30
                while timer > 0:
                    await asyncio.sleep(1)
                    timer -= 1
                    if room.u1.status == 'waiting' and room.u2.status == 'waiting':
                        break
                    if timer == 5:
                        await bot.send_message(room.u1.telegram_id, 'осталось 5 секунд')
                        await bot.send_message(room.u2.telegram_id, 'осталось 5 секунд')
                        await asyncio.sleep(5)

                texts = await manager.fight()  # Запустить битву
                await message.answer(texts.u1_text)
                await bot.send_message(user_2_id, texts.u2_text)
                await message.answer(f'ваше хп: {room.u1.hp}\nхп противника: {room.u2.hp}')
                await bot.send_message(user_2_id, texts.u2_text)
                room.round += 1


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
    if message.text:
        await message.answer('Послать можно только текстовое сообщение')
    data = await state.get_data()
    room = pvp_rooms[data.get('room')]

    if str(message.from_user.id) != room.u1.telegram_id:
        await bot.send_message(room.u1.telegram_id, f'*{room.u2.name}*: {message.text}', parse_mode='markdown')
    else:
        await bot.send_message(room.u2.telegram_id, f'*{room.u1.name}*: {message.text}', parse_mode='markdown')


# --------------------------------------------------------------------------------------------


@router.message(FightStates.move)
async def fight(message: Message, state: FSMContext):
    data = await state.get_data()
    room = pvp_rooms[data.get('room')]
    if message.from_user.id == room.u1.telegram_id:
        player = room.u1
        enemy = room.u2
    else:
        player = room.u2
        enemy = room.u1

    if message.text.lower() == 'сдаться':
        await player.state.set_state(MenuStates.main_menu)
        await enemy.state.set_state(MenuStates.main_menu)

        await bot.send_message(player.telegram_id,
                               'Вы сдались, вы вернулись в меню',
                               reply_markup=main_menu_keyboard())
        await bot.send_message(enemy.telegram_id,
                               'Противник сдался, вы вернулись в меню',
                               reply_markup=main_menu_keyboard())

    manager = SkillManager(
        u1=room.u1,
        u2=room.u2,
        history=room.moves_history,
        round=room.round
    )
    choice = await manager.choose(str(message.from_user.id), message.text)
    await message.answer(choice.text)


@router.message(FightStates.waiting)
async def wait_for_opponent(message: Message, state: FSMContext):
    data = await state.get_data()
    room = pvp_rooms[data.get('room')]
    if message.from_user.id == room.u1.telegram_id:
        player = room.u1
        enemy = room.u2
    else:
        player = room.u2
        enemy = room.u1

    if message.text.lower() == 'сдаться':
        await player.state.set_state(MenuStates.main_menu)
        await enemy.state.set_state(MenuStates.main_menu)

        await bot.send_message(player.telegram_id,
                               'Вы сдались, вы вернулись в меню',
                               reply_markup=main_menu_keyboard())
        await bot.send_message(enemy.telegram_id,
                               'Противник сдался, вы вернулись в меню',
                               reply_markup=main_menu_keyboard())

    else:
        await message.delete()
        mes = await message.answer(f'*{enemy.name}* все еще выбирает ход', parse_mode='markdown')

