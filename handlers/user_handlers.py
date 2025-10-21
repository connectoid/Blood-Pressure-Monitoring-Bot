from time import sleep

from aiogram import Bot, F, Router
from aiogram.filters.command import Command, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.types import CallbackQuery, Message, Location, FSInputFile

from aiogram.filters.state import State, StatesGroup

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage


from keyboards.main_menu import get_main_menu, get_location_menu
from keyboards.graphic_menu import get_graphic_period_menu, PeriodCallback, get_graphic_type_menu, TypeCallback
from keyboards.callback_menu import get_yes_no_menu, YesNoCallback
from config_data.config import Config, load_config
from database.orm import add_user, add_blood, get_user_id, get_bloods, add_location, get_user_data, get_user_utc
from utils.tools import (create_blood_list, create_graph, get_weather_data, get_pretty_weather, get_timezone, get_kp_data,
                         get_pretty_kp_data, check_pressure_and_pulse)

router = Router()
config: Config = load_config()
storage = MemoryStorage()


class FSMBloodState(StatesGroup):
    blood_string = State()
    blood_string_confirmed = State()

class FSMGraphState(StatesGroup):
    type = State()
    period = State()


# @router.message(~F.text)
# async def content_type_example(msg: Message):
#     await msg.answer('👍')


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
        fname = message.from_user.first_name
        lname = message.from_user.last_name
        tg_id = message.from_user.id
        start_message = f'Добро пожаловать в бот-дневник артериального давления, {fname} {lname}! Сообщите Вашу геопозицию для получения точных погодных данный. Для получения справки по работе с ботом выполните команду /help'
        greeting_message = f'Приветствую, {fname} {lname}. Для получения справки по работе с ботом выполните команду /help'
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


@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    message_text = """
Дневник артериального давления является важным инструментом самоконтроля и мониторинга состояния здоровья.
Вот основные причины, почему ведение такого дневника полезно:

- Регулярное измерение и запись показателей позволяет оценить эффективность назначенных препаратов и своевременно выявить необходимость коррекции терапии.

- Запись показаний вместе с указанием сопутствующих обстоятельств (например, погодные условия, геомагнитная обстановка) помогает определить факторы, влияющие на повышение или снижение давления.

- Иногда люди испытывают ложные колебания давления ("гипертензия белого халата"), когда давление повышается исключительно в кабинете врача. Постоянный мониторинг устраняет этот эффект и обеспечивает точные данные.

В данном боте, одновременно с ручным добавлением показателей артериального давления, автоматически добавляется множество сопутствующих факторов, таких как атмосферное давление, температура воздуха, сила и направление ветра, облачность, влажность, показатели геомагнитной обстановки и другие.

В любой момент можно посмотреть график изменения АД за любой период одновременно с графиками изменения сопутствующих факторов, для определения зависимости. 

Для точности измерений при первом запуске бота определяется ваша геопозиция и временной пояс. 

При длительной смене местанахождения рекомендуется переопределить геопозицию командой /relocate (в разработке)

    """
    await message.answer(text=message_text, reply_markup=get_main_menu())



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
        

@router.message(F.text == '❤️ Добавить', StateFilter(default_state))
async def process_blood_command(message: Message, state: FSMContext):
    await message.answer(
        text=f'Введите показатели АД и пульса в формате 120/70/75', 
        reply_markup=get_main_menu()
    )
    await state.set_state(FSMBloodState.blood_string)


@router.message(F.text,  StateFilter(FSMBloodState.blood_string))
async def process_blood_confirm_command(message: Message, state: FSMContext):
    blood_text = message.text
    if check_pressure_and_pulse(blood_text):
        values = blood_text.split('/')
        systolic_bp, diastolic_bp, pulse_rate = map(int, values)
        await message.answer(text=f'Вы ввели:\nДавление {systolic_bp} на {diastolic_bp}, пульс {pulse_rate}\nДобавить?',
                          reply_markup=get_yes_no_menu()
        )
        await state.update_data(blood_string=message.text)
        await state.set_state(FSMBloodState.blood_string_confirmed)
    else:
        await message.answer(
                text='Неверный формат строки  или неверные показатели АД и пульса. Введите в формате 120/70/75', 
                reply_markup=get_main_menu()
            )


@router.callback_query(YesNoCallback.filter(F.name == 'answer'), StateFilter(FSMBloodState.blood_string_confirmed))
async def process_add_confirmed_blood(callback: CallbackQuery, callback_data: PeriodCallback, state: FSMContext):
    tg_id = callback.from_user.id
    blood_data = await state.get_data()
    blood_text = blood_data['blood_string']

    print(callback_data)
    print(callback_data.value)
    print(blood_text)
    
    if callback_data.value == True:
        try:
            user_id, lat, lon, timezone  = get_user_data(tg_id)
            weather_data = get_weather_data(lat, lon)
            kp_data = get_kp_data(timezone)
            hi = blood_text.split('/')[0]
            low = blood_text.split('/')[1]
            pulse = blood_text.split('/')[-1]
            add_blood(hi, low, pulse, weather_data, kp_data, user_id)
            await callback.message.delete()
            await callback.message.answer(
                text='Показания добавлены', 
                reply_markup=get_main_menu()
            )
            await state.clear()
        except:
            await callback.message.answer(
                text='Ошибка при добавлении данных, обратитесь к разработчику', 
                reply_markup=get_main_menu()
            )
    else:
        await callback.message.answer(
            text=f'Введите показатели АД и пульса в формате 120/70/75', 
            reply_markup=get_main_menu()
        )
        await state.set_state(FSMBloodState.blood_string)
    


@router.message(F.text == '📈 График', StateFilter(default_state))
async def process_graphic_command(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMGraphState.type)
    await callback.answer(text='Выберите тип графика:',
                          reply_markup=get_graphic_type_menu()
        )


@router.callback_query(PeriodCallback.filter(F.name == 'mesure'), StateFilter(FSMGraphState.type))
async def process_button_type_click(callback: CallbackQuery, callback_data: TypeCallback, state: FSMContext):
    type = callback_data.value
    print(f'Type: {type}')
    await state.update_data(type=type)
    await state.set_state(FSMGraphState.period)
    await callback.message.edit_text(text='Выберите период:',
                          reply_markup=get_graphic_period_menu()
        )


@router.callback_query(PeriodCallback.filter(F.name == 'days'), StateFilter(FSMGraphState.period))
async def process_button_period_click(callback: CallbackQuery, callback_data: PeriodCallback, state: FSMContext):
    days = callback_data.value
    await state.update_data(days=days)
    graph_data = await state.get_data()
    type = graph_data['type']
    days = graph_data['days']

    tg_id = callback.from_user.id
    user_id = get_user_id(tg_id)
    utc = get_user_utc(tg_id)
    utc = utc.split('UTC')[-1]
    bloods_data = get_bloods(user_id, days)
    blood_grpaph_filename, pressure_graph_filename, kp_graph_filename, table_filename = create_graph(bloods_data, days, utc, tg_id)
    
    
    blood_file = FSInputFile(path=blood_grpaph_filename)
    pressure_file = FSInputFile(path=pressure_graph_filename)
    kp_file = FSInputFile(path=kp_graph_filename)
    media_list = [blood_file, pressure_file, kp_file, [blood_file, pressure_file, kp_file]]
    if table_filename:
        table_file = FSInputFile(path=table_filename)

    try:
        await callback.message.delete()
        if table_filename:
            await callback.message.answer_photo(
                photo=table_file,
                reply_markup=get_main_menu()
            )

        if type != 4:
            await callback.message.answer_photo(
                photo=media_list[type-1],
                # photo=blood_file,
                reply_markup=get_main_menu()
            )
            await state.clear()
        else:
            for media in media_list[:-1]:
                await callback.message.answer_photo(
                photo=media,
                # photo=blood_file,
                reply_markup=get_main_menu()
            )
            await state.clear()
    except Exception as e:
        print(f'Error with sending photo: {e}')
        await state.clear()



@router.message(F.text == '🌤 Погода', StateFilter(default_state))
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


@router.message(F.text == '🧲 Магнитные бури', StateFilter(default_state))
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

