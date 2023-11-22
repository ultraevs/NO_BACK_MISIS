from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from database import engine

Base = declarative_base()


class Operations(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    name = Column(String(200))
    number = Column(String(50))
    datee = Column(String(200))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    password = Column(String(100))
    name = Column(String(100))
    phone = Column(String(100))


Base.metadata.create_all(bind=engine)
