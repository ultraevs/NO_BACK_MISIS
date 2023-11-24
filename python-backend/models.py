from sqlalchemy import Column, Integer, String, Float, JSON, ARRAY, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
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
    email = Column(String(100))
    password_hash = Column(String(100))
    name = Column(String(100))


class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    day = Column(String(10))
    data = Column(JSON)
    tokens = Column(JSON)


class Rating(Base):
    __tablename__ = "ratings"
    email = Column(String(100), primary_key=True)
    count = Column(Integer)


Base.metadata.create_all(bind=engine)
