from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class PeriodCallback(CallbackData, prefix="period"):
        name: str
        value: int


class TypeCallback(CallbackData, prefix="type"):
        name: str
        value: int


def get_graphic_type_menu():
        bp = InlineKeyboardButton(
                text="Артериальное давление", callback_data=PeriodCallback(name="mesure", value=1).pack()
        )
        ap = InlineKeyboardButton(
                text="Атмосферное давление", callback_data=PeriodCallback(name="mesure", value=2).pack()
        )
        kp = InlineKeyboardButton(
                text="Индекс Kp", callback_data=PeriodCallback(name="mesure", value=3).pack()
        )
        all = InlineKeyboardButton(
                text="Все графики", callback_data=PeriodCallback(name="mesure", value=4).pack()
        )

        graphic_type_menu_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                        [bp],
                        [ap],
                        [kp], 
                        [all], 
                ]
        )

        return graphic_type_menu_keyboard



def get_graphic_period_menu():
        day_1 = InlineKeyboardButton(
                text="1", callback_data=PeriodCallback(name="days", value=1).pack()
        )
        day_2 = InlineKeyboardButton(
                text="2", callback_data=PeriodCallback(name="days", value=2).pack()
        )
        day_3 = InlineKeyboardButton(
                text="3", callback_data=PeriodCallback(name="days", value=3).pack()
        )
        day_4 = InlineKeyboardButton(
                text="4", callback_data=PeriodCallback(name="days", value=4).pack()
        )
        day_5 = InlineKeyboardButton(
                text="5", callback_data=PeriodCallback(name="days", value=5).pack()
        )
        day_6 = InlineKeyboardButton(
                text="6", callback_data=PeriodCallback(name="days", value=6).pack()
        )
        week_button = InlineKeyboardButton(
                text="Неделя", callback_data=PeriodCallback(name="days", value=7).pack()
        )
        day_10 = InlineKeyboardButton(
                text="10 дней", callback_data=PeriodCallback(name="days", value=10).pack()
        )
        month_button = InlineKeyboardButton(
                text="Месяц", callback_data=PeriodCallback(name="days", value=30).pack()
        )

        graphic_period_menu_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                        [day_1, day_2, day_3],
                        [day_4, day_5, day_6],
                        [week_button], 
                        [day_10], 
                        [month_button], 
                ]
        )

        return graphic_period_menu_keyboard
