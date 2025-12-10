from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# SQLite 데이터베이스 URL (파일은 mission-4-8 폴더에 생성됩니다)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./questions.db'

# SQLite 사용 시 check_same_thread=False 필요
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

# autocommit은 False로 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """DB 세션을 yield하고 사용이 끝나면 닫아 준다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
