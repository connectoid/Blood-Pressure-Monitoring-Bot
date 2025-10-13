from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_graphic_menu():

        week_button = InlineKeyboardButton(
                text="Неделя", callback_data="week_button_click"
        )
        month_button = InlineKeyboardButton(
                text="Месяц", callback_data="month_button_click"
        )
        year_button = InlineKeyboardButton(
                text="Год", callback_data="year_button_click"
        )

        graphic_menu_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[week_button], [month_button], [year_button]]
        )

        return graphic_menu_keyboard
