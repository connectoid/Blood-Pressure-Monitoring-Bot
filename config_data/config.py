from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных
    

@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту 
    admin_chat_id: str


@dataclass
class Payment:
    paymen_provider_token: str


@dataclass
class OpenWeather:
    weather_token: str
    utc_token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    payment: Payment
    open_weather: OpenWeather


def load_config(path: str = None):

    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_chat_id=env('ADMIN_CHAT_ID')),
                    db=DatabaseConfig(database=env('DATABASE'),
                                    db_host=env('DB_HOST'),
                                    db_user=env('DB_USER'),
                                    db_password=env('DB_PASSWORD')),
                    payment=Payment(paymen_provider_token=env('PAYMENTS_PROVIDER_TOKEN')),
                    open_weather=OpenWeather(weather_token=env('OPEN_WEATHER_API_TOKEN'),
                                            utc_token=env('BIGDATA_UTC_API_TOKEN')),
                    )
