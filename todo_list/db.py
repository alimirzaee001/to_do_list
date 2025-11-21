"""
Database setup for the ToDo List application.

Configures SQLAlchemy engine, session factory, and declarative base.
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from .config import config

Base = declarative_base()

# echo=False to avoid noisy logs; can be overridden via env if needed
engine = create_engine(config.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, class_=Session, future=True)


@contextmanager
def get_session() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
