from sqlmodel import Session, create_engine
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@contextmanager
def getSession():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
