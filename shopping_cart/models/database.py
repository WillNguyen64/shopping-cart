from contextlib import contextmanager

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..common.settings import get_settings


settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.db_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=settings.db_trace,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# This is used to inject a DB session to a FastAPI path operation to perform
# CRUD operations on the DB.
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This is used to provide a DB session to other places in the code that need to
# perform CRUD operations on the DB, such as long-running background tasks that
# need to update a DB record.
@contextmanager
def get_db_session_ctx_mgr():
    return get_db_session()
