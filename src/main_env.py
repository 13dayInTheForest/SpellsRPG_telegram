from aiogram.fsm.storage.memory import MemoryStorage
from src.domain.rooms.interface import IRoom

storage = MemoryStorage()

""" Очередь на поиск """
waiting_users = []

""" 
    Комнаты где происходят активные PVP бои
    {'first_id + _ + second_id': Room} 
"""
pvp_rooms: dict[str, IRoom] = {}
