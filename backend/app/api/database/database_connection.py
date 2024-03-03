from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://apl_apimigration:apl123UseR@localhost/migrationdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()