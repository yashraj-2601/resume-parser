from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

_engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

def init_db(database_url: str):
    global _engine, SessionLocal
    _engine = create_engine(database_url, future=True)
    SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
    from .models import Candidate
    Base.metadata.create_all(_engine)

def get_session():
    return SessionLocal()
