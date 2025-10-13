from time import sleep

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message, Location

from aiogram.filters.state import State, StatesGroup

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage


from keyboards.main_menu import get_main_menu, get_location_menu
from keyboards.graphic_menu import get_graphic_menu
from config_data.config import Config, load_config
from database.orm import add_user, add_blood, get_user_id, get_bloods, add_location, get_user_data
from utils.tools import (create_graphic, get_weather_data, get_pretty_weather, get_timezone, get_kp_data,
                         get_pretty_kp_data, check_pressure_and_pulse)

router = Router()
config: Config = load_config()
storage = MemoryStorage()


class FSMBloodState(StatesGroup):
    blood_string = State()

class FSMGraphState(StatesGroup):
    period = State()


# @router.message(~F.text)
# async def content_type_example(msg: Message):
#     await msg.answer('👍')


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
        fname = message.from_user.first_name
        lname = message.from_user.last_name
        tg_id = message.from_user.id
        start_message = f'Добро пожаловать, {fname} {lname}! Сообщите Вашу геопозицию для получения точных погодных данный.'
        greeting_message = f'Hello, {fname} {lname}'
        new_user = False
        if add_user(tg_id, fname, lname):
            new_user = True
        if new_user:
            await message.answer(
            text=start_message,
            reply_markup=get_location_menu())
        else:
            await message.answer(
            text=greeting_message,
            reply_markup=get_main_menu())


@router.message(F.location.as_("location"))
async def process_location(message: Message, location: Location) -> None:
    latitude = location.latitude
    longitude = location.longitude
    tg_id = message.from_user.id
    timezone = get_timezone(latitude, longitude)
    if timezone:
        add_location(tg_id, latitude, longitude, timezone)
        await message.answer(
            text=f'Ваша геопозиция: Широта {latitude:.6f}, Долгота {longitude:.6f}',
            reply_markup=get_main_menu())
    else:
        await message.answer(
            text=f'Ошибка получения временной зоны (UTC)',
            reply_markup=get_main_menu())
        

@router.message(Text(text='❤️ Добавить'), StateFilter(default_state))
async def process_blood_command(message: Message, state: FSMContext):
    await message.answer(
        text=f'Введите показатели АД и пульса в формате 120/70/75', 
        reply_markup=get_main_menu()
    )
    await state.set_state(FSMBloodState.blood_string)


@router.message(Text,  StateFilter(FSMBloodState.blood_string))
async def process_text_command(message: Message, state: FSMContext):
    await state.update_data(blood_string=message.text)
    tg_id = message.from_user.id
    blood_text = message.text # 120/70/72
    if check_pressure_and_pulse(blood_text):
        try:
            user_id, lat, lon, timezone  = get_user_data(tg_id)
            weather_data = get_weather_data(lat, lon)
            kp_data = get_kp_data(timezone)
            hi = blood_text.split('/')[0]
            low = blood_text.split('/')[1]
            pulse = blood_text.split('/')[-1]
            add_blood(hi, low, pulse, weather_data, kp_data, user_id)
            await message.answer(
                text='Показания добавлены', 
                reply_markup=get_main_menu()
            )
            await state.clear()
        except:
            await message.answer(
                text='Ошибка при добавлении данных, обратитесь к разработчику', 
                reply_markup=get_main_menu()
            )
    else:
        await message.answer(
                text='Неверный формат строки  или неверные показатели АД и пульса. Введите в формате 120/70/75', 
                reply_markup=get_main_menu()
            )


@router.message(Text(text='📈 График'), StateFilter(default_state))
async def process_graphic_command(callback: CallbackQuery):
    await callback.answer(text='Выберите период:',
                          reply_markup=get_graphic_menu()
        )


@router.callback_query(F.data == 'week_button_click')
async def process_button_1_click(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user_id = get_user_id(tg_id)
    bloods_data = get_bloods(user_id)
    graphic = create_graphic(bloods_data)
    await callback.message.answer(
            text='График за неделю', 
            reply_markup=get_main_menu()
        )



@router.message(Text(text='🌤 Погода'), StateFilter(default_state))
async def process_blood_command(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user_id, lat, lon, timezone = get_user_data(tg_id)
    print(lat, lon)
    weather_data = get_weather_data(lat, lon)
    pretty_weather_data = get_pretty_weather(weather_data)
    await message.answer(
        text=pretty_weather_data, 
        reply_markup=get_main_menu()
    )


@router.message(Text(text='🧲 Магнитные бури'), StateFilter(default_state))
async def process_blood_command(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user_id, lat, lon, timezone = get_user_data(tg_id)
    print(timezone)
    kp_data = get_kp_data(timezone)
    pretty_kp_data = get_pretty_kp_data(kp_data)
    await message.answer(
        text=pretty_kp_data, 
        reply_markup=get_main_menu()
    )

