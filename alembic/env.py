"""
alembic env.py for BizStack Perks
This config loads SQLAlchemy URL from DATABASE_URL env var and uses the
models.Base.metadata for autogenerate support.
"""
from __future__ import with_statement
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.db import Base  # noqa: E402
from api.models import *  # noqa: E402,F401 - registers models on Base

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired: config.get_main_option("some_option")
#
# If DATABASE_URL is provided in environment, use that; otherwise fallback
sqlalchemy_url = os.environ.get('DATABASE_URL')
if sqlalchemy_url:
    config.set_main_option('sqlalchemy.url', sqlalchemy_url)


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
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
