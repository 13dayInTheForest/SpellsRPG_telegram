from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def skills_buttons(all_skills: list):
    buttons = [[KeyboardButton(text=name)] for name in all_skills]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )