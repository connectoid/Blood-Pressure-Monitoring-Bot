from datetime import datetime, timedelta

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from .models import Base, User, Blood
from config_data.config import load_config, Config

POOL_SIZE = 20
MAX_OVERFLOW = 0

config: Config = load_config()

db_user = config.db.db_user
db_password = config.db.db_password

database_url = f'postgresql://{db_user}:{db_password}@{config.db.db_host}:5432/{config.db.database}'

engine = create_engine(database_url, echo=False, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_blood(hi, low, pulse, weather_data, kp_data, owner):
    session = Session()
    new_blood = Blood(
            # blood data
            hi=hi,
            low=low,
            pulse=pulse,
            owner=owner,
            # weather data
            pressure_mm=weather_data['pressure_mm'],
            humidity=weather_data['humidity'],
            temp=weather_data['temp'],
            wind=weather_data['wind'],
            wind_direction=weather_data['wind_direction'],
            clouds=weather_data['clouds'],
            visibility=weather_data['visibility'],
            last_kp_index=kp_data['last_kp'],
            max_kp_index=kp_data['max_kp'],
        )
    session.add(new_blood)
    session.commit()


def get_bloods(owner, days):
    today = datetime.now()
    time_edge = today - timedelta(days=days)
    print(today)
    print(time_edge)
    session = Session()
    bloods = session.query(Blood).filter(Blood.owner == owner).filter(Blood.register_date >= time_edge)
    return bloods


def add_user(tg_id, fname, lname):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(
            tg_id=tg_id,
            fname=fname, 
            lname=lname,)
        session.add(new_user)
        session.commit()
        return True
    return False 


def add_location(tg_id, lat, lon, timezone):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.location_lat=lat
    user.location_lon=lon
    user.timezone=timezone
    session.add(user)
    session.commit()


def get_user_id(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.id


def get_user_utc(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.timezone


def get_user_data(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user_id = user.id
    lat = user.location_lat
    lon = user.location_lon
    timezone = user.timezone
    return user_id, lat, lon, timezone


