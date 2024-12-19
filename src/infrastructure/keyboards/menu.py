from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Бой')],
            [KeyboardButton(text='Магазин'), KeyboardButton(text='Статистика')]
        ],
        resize_keyboard=True
    )


def shop_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Контракты')],
            [KeyboardButton(text='Экипировка')],
            [KeyboardButton(text='Классы')]
        ],
        resize_keyboard=True
    )


def gods_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Зевс', callback_data='god_zeus')],
            [InlineKeyboardButton(text='Афина', callback_data='god_afina')],
            [InlineKeyboardButton(text='Аматэрасу', callback_data='god_amaterasu')],
            [InlineKeyboardButton(text='Арес', callback_data='god_ares')],
            [InlineKeyboardButton(text='<-', callback_data='god_go_back'),
             InlineKeyboardButton(text='->', callback_data='god_go_next')],
            [InlineKeyboardButton(text='В меню', callback_data='god_go_exit')]
        ]
    )


