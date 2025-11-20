from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
import sys

# 프로젝트 경로를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 프로젝트의 `database` 모듈에서 `Base`를 가져오고 `models`를 임포트하여
# `Base.metadata`에 테이블 정의가 포함되도록 보장한다.
from database import Base  # noqa: E402
import models  # noqa: E402,F401

config = context.config
try:
    fileConfig(config.config_file_name)
except Exception:
    # 단순화된 설정에서는 alembic.ini에 로깅 섹션이 없을 수 있다
    pass

# 설정에 `sqlalchemy.url`이 없으면 로컬 SQLite 파일로 대체하도록 설정한다
if not config.get_main_option('sqlalchemy.url'):
    config.set_main_option('sqlalchemy.url', 'sqlite:///./questions.db')

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url')
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
