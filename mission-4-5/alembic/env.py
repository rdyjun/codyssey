from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
import sys

# 프로젝트 경로를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Base from the project's database module and ensure models
# are imported so that `Base.metadata` contains table definitions.
from database import Base  # noqa: E402
import models  # noqa: E402,F401

config = context.config
try:
    fileConfig(config.config_file_name)
except Exception:
    # alembic.ini may not contain logging sections in this simplified setup
    pass

# Ensure sqlalchemy.url is present in config (fallback to local sqlite file)
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
