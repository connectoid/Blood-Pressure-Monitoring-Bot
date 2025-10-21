import json
import requests
from pprint import pprint
import os
import pytz

import matplotlib.pyplot as plt
from matplotlib.table import Table
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
AutoMinorLocator)

from config_data.config import Config, load_config

config: Config = load_config()
ow_token = config.open_weather.weather_token
utc_token = config.open_weather.utc_token

PRESSURE_FACTOR = 0.007501
MAX_DATES_COUNT = 14
graph_path = './files/'
code_timezone_file = 'code_timezone.json'


wind_directions = {
    0: 'Северный',
    45: 'Северо-восточный',
    90: 'Восточный',
    135: 'Юго-восточный',
    180: 'Южный',
    225: 'Юго-западный',
    270: 'Западный',
    315: 'Северо-западный',
    360: 'Северный',
}


def get_direction(deg):
    directions = [0, 45, 90, 135, 180, 225, 270, 315, 360]
    min = 360
    for true_deg in directions:
        print(f'{true_deg} - {deg} = {abs(true_deg - deg)}')
        print(f'{abs(true_deg - deg)} < {min}')
        if (abs(true_deg - deg)) < min:
            true_direction = true_deg
            min = abs(true_deg - deg)
            print(true_direction)
    return true_direction


def plot_pressure_graph(pressure: list, dates: list, days: int, tg_id):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title(f'График атмосферного давления за {days} д.', fontsize=16)
        ax.set_xlabel('Измерения атмосферного давления', fontsize=14)
        ax.set_ylabel('Показатели атмосферного давления, мм', fontsize=14)
        ax.grid(which='major', linewidth=1.2)
        ax.grid(which='minor', linestyle='--', color='gray', linewidth=0.5)
        # ax.scatter(x, y1, c='red', label='y1 = 4*x')
        ax.plot(dates, pressure, label='Атмосферное давление, мм')
        ax.legend()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='major', length=10, width=2)
        ax.tick_params(which='minor', length=5, width=1)
        if not os.path.exists('./files'):
            os.mkdir('./files')
        graph_pressure_filename = graph_path + str(tg_id) + '_pressure_plot.png'
        
        plt.savefig(graph_pressure_filename, dpi=200)
        return graph_pressure_filename


def plot_kp_graph(last_kp: list, dates: list, days: int, tg_id):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title(f'График индекса Kp за {days} д.', fontsize=16)
        ax.set_xlabel('Измерения', fontsize=14)
        ax.set_ylabel('Показатели', fontsize=14)
        ax.grid(which='major', linewidth=1.2)
        ax.grid(which='minor', linestyle='--', color='gray', linewidth=0.5)
        # ax.scatter(x, y1, c='red', label='y1 = 4*x')
        ax.plot(dates, last_kp, label='Индекс Kp, мм')
        ax.legend()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='major', length=10, width=2)
        ax.tick_params(which='minor', length=5, width=1)
        if not os.path.exists('./files'):
            os.mkdir('./files')
        graph_kp_filename = graph_path + str(tg_id) + '_kp_plot.png'
        
        plt.savefig(graph_kp_filename, dpi=200)
        return graph_kp_filename



def plot_blood_graph(hi: list, low: list, pulse: list, dates: list, days: int, tg_id):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title(f'График артетриального давления за {days} д.', fontsize=16)
        ax.set_xlabel('Измерения артериального давления', fontsize=14)
        ax.set_ylabel('Показатели артериального давления', fontsize=14)
        ax.grid(which='major', linewidth=1.2)
        ax.grid(which='minor', linestyle='--', color='gray', linewidth=0.5)
        # ax.scatter(x, y1, c='red', label='y1 = 4*x')
        ax.plot(dates, hi, label='Верхнее давление')
        ax.plot(dates, low, label='Нижнеее давление')
        ax.plot(dates, pulse, label='Пульс')
        ax.legend()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='major', length=10, width=2)
        ax.tick_params(which='minor', length=5, width=1)

        if not os.path.exists('./files'):
            os.mkdir('./files')
        graph_blood_filename = graph_path + str(tg_id) + '_blood_plot.png'
        
        plt.savefig(graph_blood_filename, dpi=200)
        return graph_blood_filename


def save_dictionary_as_png(data_dict, tg_id):
    filename = graph_path + str(tg_id) + '_table.png'
    fig, ax = plt.subplots()
    ax.axis('off')

    headers = ["Номер измерения", "Дата и время"]
    table_data = []

    for number, date in sorted(data_dict.items()):
        table_data.append([number, date])

    table_data.insert(0, headers)

    tb = Table(ax, bbox=[0, 0, 1, 1])
    nrows, ncols = len(table_data), len(table_data[0])
    width, height = 1 / ncols, 1 / nrows

    colors = [['#F0FFFF'] * ncols] + [['#DCDCDC']*ncols]*nrows
    colors.pop(-1) 

    for i in range(nrows):
        for j in range(ncols):
            tb.add_cell(i, j, width, height, text=table_data[i][j], loc='center', facecolor=colors[i][j])

    tb.auto_set_font_size(False)
    tb.set_fontsize(12)
    tb.scale(1, 1.5)

    ax.add_table(tb)

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return filename



def create_graph(blood_data, days, utc, tg_id):
    timezone = pytz.timezone(f'Etc/GMT{utc}')
    table_filename = ''
    hi_blood = [blood.hi for blood in blood_data]
    low_blood = [blood.low for blood in blood_data]
    pulse = [blood.pulse for blood in blood_data]
    pressures_mm = [blood.pressure_mm for blood in blood_data]
    last_kp = [blood.last_kp_index for blood in blood_data]

    date_numbers = [i for i in range(1, len(hi_blood)+1)]
    dates_values = [date.register_date.astimezone(timezone).strftime("%d.%m %H:%M") for date in blood_data]
    dates_values_short = [date.split()[0] + '\n' + date.split()[-1] for date in dates_values]
    dates_dict = dict(zip(date_numbers, dates_values))
    

    if len(hi_blood) > MAX_DATES_COUNT:
        dates = date_numbers
        table_filename = save_dictionary_as_png(dates_dict, tg_id)
    else:
        dates = dates_values_short

    blood_graph_filename = plot_blood_graph(hi_blood, low_blood, pulse, dates, days, tg_id)
    pressure_graph_filename = plot_pressure_graph(pressures_mm, dates, days, tg_id)
    kp_graph_filename = plot_kp_graph(last_kp, dates, days, tg_id)
    print(f'table_filename: {table_filename}')
    return blood_graph_filename, pressure_graph_filename, kp_graph_filename, table_filename



def create_blood_list(blood_data, days):
    print(f'Создаем график за {days} дней')
    count = 0
    pretty_blood_list = []
    for blood in blood_data:
        if count >= days:
            break

        regdate = blood.register_date
        formatted_date_time = regdate.strftime("%d.%m.%Y %H:%M")

        hi = blood.hi
        low = blood.low
        pulse = blood.pulse

        # weather data
        pressure_mm=blood.pressure_mm
        humidity=blood.humidity
        temp=blood.temp
        wind=blood.wind
        wind_direction=blood.wind_direction
        wind_real_direction = get_direction(wind_direction)
        wind_real_direction = wind_directions[wind_real_direction]
        clouds=blood.clouds
        visibility=blood.visibility
        last_kp_index=blood.last_kp_index
        max_kp_index=blood.max_kp_index

        pretty_blood_string = f"""
Дата: {formatted_date_time}

Верхнее АД: {hi}
Нижнее АД: {low}
Пульс: {pulse}

Атм. давление: {pressure_mm} мм
Влажность: {humidity} %
Температура: {temp} ˚C
Ветер: {wind} м/с
Направление ветра: {wind_real_direction} {wind_direction} ˚
Облачность: {clouds} %
Видимость: {visibility} м
Последний Kp-индекс: {last_kp_index}
Макс. Kp-индекс: {max_kp_index}
        """
        pretty_blood_list.append(pretty_blood_string)
        print(pretty_blood_string)
        count += 1

    message_text = ('\n').join(pretty_blood_list)
    return message_text


def get_weather_data(lat, lon):
    print(f'Получаем погодные данные по координатам {lat} {lon}')
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={ow_token}&units=metric&lang=ru'
    response = requests.get(url)
    if response.status_code == 200:
        weather_data_row = response.text
        try:
            weather_data = {}
            parsed_weather = json.loads(weather_data_row)
            name = parsed_weather['name']
            description = parsed_weather['weather'][0]['description']
            humidity = parsed_weather['main']['humidity']
            pressure_hPa = parsed_weather['main']['pressure']
            pressure_mm = int(pressure_hPa * PRESSURE_FACTOR * 100)
            temp = parsed_weather['main']['temp']
            temp_feels_like = parsed_weather['main']['feels_like']
            wind = parsed_weather['wind']['speed']
            wind_direction = parsed_weather['wind']['deg']
            clouds = parsed_weather['clouds']['all']
            visibility = parsed_weather['visibility']
            weather_data['name'] = name
            weather_data['description'] = description.capitalize()
            weather_data['pressure_hPa'] = pressure_hPa
            weather_data['pressure_mm'] = pressure_mm
            weather_data['temp'] = round(temp)
            weather_data['temp_feels_like'] = round(temp_feels_like)
            weather_data['humidity'] = humidity
            weather_data['wind'] = wind
            weather_data['wind_direction'] = wind_direction
            wind_real_direction = get_direction(wind_direction)
            weather_data['wind_real_direction'] = wind_directions[wind_real_direction]
            weather_data['clouds'] = clouds
            weather_data['visibility'] = visibility
            pprint(weather_data)
            return weather_data
        except Exception as e:
            print(f'Ошибка получения погодных данных: {e}')
            return None
    else:
        print(f'Request error {response.status_code}')
        return None


def get_code_by_timezone(timezone):
    code = ''
    with open(code_timezone_file, 'r') as file:
        data = json.load(file)
    code = data[timezone]
    return code


def get_kp_data(timezone):
    print(f'Получаем данные магнитных бурь по времени {timezone}')

    code = get_code_by_timezone(timezone)
    url = f'https://xras.ru/txt/kp_{code}.json'

    response = requests.get(url)
    if response.status_code == 200:
        hours_1 = ['h0'+str(h) for h in range(0, 10)]
        hours_2 = ['h'+str(h) for h in range(10, 25)]
        hours = hours_1 + hours_2

        json_data = response.json()
        max_kp = json_data['data'][0]['max_kp']
        date = json_data['data'][0]['time']
        time_zone = json_data['tzone']
        all_kp_data = json_data['data'][0]

        kp_by_hours = {key: all_kp_data[key] for key in hours if (key in all_kp_data) and (all_kp_data[key] != 'null')}

        # print(kp_by_hours)
        kp_data = {}
        kp_data['max_kp'] = max_kp
        kp_data['date'] = date
        kp_data['time_zone'] = time_zone
        kp_data['time_zone_utc'] = time_zone.split('(')[-1].split(')')[0]
        kp_data['kp_by_hours'] = kp_by_hours
        last_kp_index = 0
        for index in kp_by_hours.values():
            if (index != 'null'):
                if float(index) > 0:
                    last_kp_index = index
        kp_data['last_kp'] = last_kp_index
        return kp_data
    else:
        print(f'Error: {response.status_code}')
        return None


def get_pretty_weather(weather_data):
    pretty_weather_string = f"""
Текущая погода:
Населенный пункт: {weather_data['name']}
Погодные условия: {weather_data['description']}
Температура: {weather_data['temp']}˚C
Ощущается: {weather_data['temp_feels_like']}˚C
Ветер: {weather_data['wind']} м/с
Направление: {weather_data['wind_real_direction']}, {weather_data['wind_direction']}˚
Облачность: {weather_data['clouds']} %
Видимость: {weather_data['visibility']} метров
Атмосферное давление: {weather_data['pressure_mm']} мм. рт. ст.
Влажность: {weather_data['humidity']}%
    """
    return pretty_weather_string


def get_pretty_kp_data(kp_data):
    kp_by_hours = []
    for key, value in kp_data['kp_by_hours'].items():
        hour = key[1:] + ':00'
        hour_kp = f'{hour}: {value}'
        kp_by_hours.append(hour_kp)
        kp_by_hours_string = ' '.join(kp_by_hours)
        timezone = kp_data['time_zone'].split('(')[-1][:-1]
    pretty_kp_string = f"""
Текущая геомагнитная обстановка:
Часовой пояс: {kp_data['time_zone']}
Текущая дата по UTC: {kp_data['date']}
Макс. индекс KP за сутки: {kp_data['max_kp']}
Почасовой индекс КП: {kp_by_hours_string}
Последний индекс КП: {kp_data['last_kp']}
    """
    return pretty_kp_string


def get_timezone(lat, lon):
    print(f'Получаем временную зону по координатам {lat} {lon}')
    # lat = '-34.9313'
    # lon = '138.59669'

    url = f'https://api-bdc.net/data/timezone-by-location?latitude={lat}&longitude={lon}&key={utc_token}'
    response = requests.get(url)
    print(response.json())
    if response.status_code == 200:
        timezone = response.json()['utcOffset']
        timezone = normalize_timezone(timezone)
        return timezone
    else:
        print(f'Error in get)timezone: {response.status_code}')
        return None


def normalize_timezone(timezone: str):
    timezone = timezone.replace('30', '00')
    timezone = timezone.replace(':00', '')
    if timezone.find('UTC') == -1:
        timezone = 'UTC' + timezone
    return timezone


def check_pressure_and_pulse(input_string):
    try:
        values = input_string.split('/')
        if len(values) != 3:
            return False
        systolic_bp, diastolic_bp, pulse_rate = map(int, values)
        valid_pressure_range = (systolic_bp > 0 and systolic_bp <= 300 and 
                                diastolic_bp >= 0 and diastolic_bp < systolic_bp)
        valid_pulse_range = (pulse_rate > 0 and pulse_rate <= 250)
        return valid_pressure_range and valid_pulse_range
    except ValueError:
        return False
