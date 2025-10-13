from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, BigInteger, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
 
 
class Blood(Base):
    __tablename__ = 'blood'
    id = Column(Integer, primary_key=True)
    low = Column(Integer, nullable=False)
    hi = Column(Integer, nullable=False)
    pulse = Column(Integer, nullable=False)

    # weather data
    pressure_mm = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    temp = Column(Integer, nullable=False)
    wind = Column(Integer, nullable=False)
    wind_direction = Column(Integer, nullable=False)
    clouds = Column(Integer, nullable=False)
    visibility = Column(Integer, nullable=False)
    last_kp_index = Column(Float, nullable=False)
    max_kp_index = Column(Float, nullable=False)

    owner = Column(Integer, ForeignKey('user.id'), nullable=False)
    register_date = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return self.id


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    fname = Column(String, nullable=True)
    lname = Column(String, nullable=True)
    tg_id = Column(BigInteger, nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    timezone = Column(String, nullable=True)
    bloods = relationship('Blood', backref='users', lazy=True)
    register_date = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return self.tg_id
