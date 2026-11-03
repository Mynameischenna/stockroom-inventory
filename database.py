import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()  # reads .env into environment variables (like application.properties)

DATABASE_URL = os.environ["DATABASE_URL"]  # fails fast if not set

engine = create_engine(DATABASE_URL)  # connection to postgres (like spring.datasource.url)
SessionLocal = sessionmaker(bind=engine, autoflush=False)  # factory that creates sessions (like EntityManager)


class Base(DeclarativeBase):  # all table models inherit from this
    pass


def get_db():
    # gives one session per request and always closes it afterwards
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
