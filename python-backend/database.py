from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://cu41662_urbaton:urbaton@5.23.50.27/cu41662_urbaton"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)


def get_db() -> Generator[Session, None, None]:
    db = Session(engine)
    yield db
