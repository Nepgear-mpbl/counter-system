# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, text
from counterSystem import db


Base = db.Model
metadata = Base.metadata


class Busines(Base):
    __tablename__ = 'business'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    counter_id = Column(Integer)
    valid = Column(Integer, nullable=False, server_default=text("'1'"))
    post_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Counter(Base):
    __tablename__ = 'counter'

    counter_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(12), nullable=False)
    pwd = Column(String(20), nullable=False)
    salt = Column(String(32), nullable=False)
    last_login_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    type = Column(Integer, nullable=False, server_default=text("'1'"))
