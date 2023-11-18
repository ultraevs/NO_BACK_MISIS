from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@45.89.190.31/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)


def get_db() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()