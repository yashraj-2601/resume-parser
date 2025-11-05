from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

_engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

def _ensure_ssl(url: str) -> str:
    # add sslmode=require if missing
    parsed = urlparse(url)
    q = parse_qs(parsed.query)
    if "sslmode" not in q:
        q["sslmode"] = ["require"]
        parsed = parsed._replace(query=urlencode(q, doseq=True))
    # normalize scheme to postgresql+psycopg2
    scheme = "postgresql+psycopg2"
    if not parsed.scheme.startswith("postgresql"):
        parsed = parsed._replace(scheme=scheme)
    return urlunparse(parsed)

def init_db(database_url: str):
    global _engine, SessionLocal
    database_url = _ensure_ssl(database_url)
    _engine = create_engine(database_url, future=True)
    SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
    from .models import Candidate  # noqa
    Base.metadata.create_all(_engine)

def get_session():
    return SessionLocal()
