from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 데이터베이스 URL (파일은 mission-4-6 폴더에 생성됩니다)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./questions.db'

# SQLite 사용 시 check_same_thread=False 필요
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

# autocommit은 False로 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """DB 세션을 yield하고 요청 종료 시 세션을 닫아 준다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
