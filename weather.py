from utils.tools import get_weather, get_pretty_weather


weather_data = get_weather('64.4213', '-173.2354')
pretty_weather = get_pretty_weather(weather_data)
print(pretty_weather)