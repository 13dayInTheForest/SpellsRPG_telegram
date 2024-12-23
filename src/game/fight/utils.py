import asyncio
from src.infrastructure.bot import bot
from src.domain.rooms.interface import IRoom


async def timer_task(time: int, room: IRoom):
    try:
        await asyncio.sleep(time - 5)
        await bot.send_message(room.u1.telegram_id, 'осталось 5 секунд')
        await bot.send_message(room.u2.telegram_id, 'осталось 5 секунд')
        await asyncio.sleep(5)
        room.u1.status = 'moving'
        room.u2.status = 'moving'
    except asyncio.CancelledError:
        room.u1.status = 'moving'
        room.u2.status = 'moving'


