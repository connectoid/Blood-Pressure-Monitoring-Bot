from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)



def get_main_menu():
    button_1: KeyboardButton = KeyboardButton(text='❤️ Добавить')
    button_2: KeyboardButton = KeyboardButton(text='📈 График')
    button_3: KeyboardButton = KeyboardButton(text='🌤 Погода')
    button_4: KeyboardButton = KeyboardButton(text='🧲 Магнитные бури')

    main_menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_1, button_2],
                                                [button_3, button_4]],
                                        resize_keyboard=True,
                                        input_field_placeholder='placeholder')
    return main_menu_keyboard


def get_location_menu():
    print('Creating location menu')
    location_menu = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Поделиться моим местоположением 📍", request_location=True),
        ]
    ], resize_keyboard=True)
    return location_menu
