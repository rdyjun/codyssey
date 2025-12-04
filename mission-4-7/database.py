from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# SQLite 데이터베이스 URL (파일은 mission-4-7 폴더에 생성됩니다)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./questions.db'

# SQLite 사용 시 check_same_thread=False 필요
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

# autocommit은 False로 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db_cm() -> Generator[Session, None, None]:
    """contextmanager로 구현된 DB 세션 생성기.

    실제 세션 생성/종료는 이 컨텍스트 매니저에서 처리되며,
    FastAPI 의존성에서는 아래의 `get_db` 제너레이터 래퍼를 사용한다.
    """
    db = SessionLocal()
    try:
        print('DB 연결: 세션 시작')
        yield db
    finally:
        db.close()
        print('DB 연결 종료: 세션 닫음')


def get_db() -> Generator[Session, None, None]:
    """FastAPI 의존성에서 사용할 제너레이터 래퍼.

    내부적으로 `get_db_cm` 컨텍스트 매니저를 사용하여 세션을 열고
    `yield`로 제공한 뒤 자동으로 종료한다. 이렇게 하면
    contextlib.contextmanager를 이용하면서도 FastAPI가 기대하는
    제너레이터 형태의 의존성 인터페이스를 제공할 수 있다.
    """
    with get_db_cm() as db:
        yield db
