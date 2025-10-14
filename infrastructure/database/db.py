import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.sqlalchemy import Base

database_url = os.getenv("DATABASE_URL", "sqlite:///./items.db")

engine = create_engine(database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    Base.metadata.create_all(bind=engine)
