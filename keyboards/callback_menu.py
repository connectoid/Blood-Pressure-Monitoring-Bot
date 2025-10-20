from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class YesNoCallback(CallbackData, prefix="answer"):
        name: str
        value: bool



def get_yes_no_menu():
        yes_button = InlineKeyboardButton(
                text="Да", callback_data=YesNoCallback(name="answer", value=True).pack()
        )
        no_button = InlineKeyboardButton(
                text="Нет", callback_data=YesNoCallback(name="answer", value=False).pack()
        )

        yes_no_menu_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                        [yes_button, no_button],
                ]
        )

        return yes_no_menu_keyboard
