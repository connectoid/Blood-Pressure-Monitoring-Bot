import requests
import json
from pprint import pprint
import os

from bs4 import BeautifulSoup

url = 'https://xras.ru/txt/kp_SSWT.json'
pic_url = 'https://xras.ru/image/kp_SSWT.png'

main_url = 'https://xras.ru/magnetic_storms.html'

code_timezone_file = 'code_timezone.json'
code_timezone_file_tmp = 'code_timezone_tmp.json'

def get_regions():
    html_file = 'tmp.html'

    with open(html_file, encoding='utf-8') as f:    
        content = f.read()

    soup = BeautifulSoup(content, 'lxml')
    regions = soup.find('select', {'id': 'region'}).find_all('option')
    reg_codes = []
    for region in regions:
        reg_code = {}
        reg_code['region'] = region.text
        reg_code['code'] = region['value']
        reg_codes.append(reg_code)
    reg_codes = reg_codes[1:]
    code_timezone = {}
    for reg_code in reg_codes:
        code = reg_code['code']
        time_zone_utc = get_kp_index(f'https://xras.ru/txt/kp_{code}.json')['time_zone_utc']
        print(f'https://xras.ru/txt/kp_{code}.json')
        print(f'Code {code}: {time_zone_utc}')
        code_timezone[time_zone_utc] = code
        # code_timezone['timezone'] = time_zone_utc
        # code_timezone_list.append(code_timezone)
    with open(code_timezone_file_tmp, 'w', encoding='utf-8') as file:
        json.dump(code_timezone, file, ensure_ascii=False, indent=4)

def get_code_by_timezone(timezone):
    code = ''
    with open(code_timezone_file, 'r') as file:
        data = json.load(file)
    code = data[timezone]
    return code


def get_kp_index(url):

    response = requests.get(url)
    if response.status_code == 200:
        hours = ["h00", "h03", "h06", "h09", "h12", "h15", "h18", "h21"]

        json_data = response.json()
        max_kp = json_data['data'][0]['max_kp']
        date = json_data['data'][0]['time']
        time_zone = json_data['tzone']
        all_kp_data = json_data['data'][0]

        # Фильтруем словарь
        kp_by_hours = {key: all_kp_data[key] for key in hours if key in all_kp_data}

        # print(kp_by_hours)
        kp_data = {}
        kp_data['max_kp'] = max_kp
        kp_data['date'] = date
        kp_data['time_zone'] = time_zone
        kp_data['time_zone_utc'] = time_zone.split('(')[-1].split(')')[0]
        kp_data['kp_by_hours'] = kp_by_hours
        return kp_data
    else:
        print(f'Error: {response.status_code}')


# kp_data = get_kp_index(url)
# pprint(kp_data)
# get_regions()

code = get_code_by_timezone('UTC+10')
print(code)