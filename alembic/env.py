from logging.config import fileConfig

from app.marketplace.models.models import Base

target_metadata = Base.metadata

from sqlalchemy import create_engine, pool
from sqlalchemy.engine import Connectable, Engine

from alembic import context
from common.settings import database_settings

from app.marketplace.models.models import (
    ShopUnit,
)

target_metadata = ShopUnit.metadata

config = context.config

fileConfig(config.config_file_name)


def run_migrations_offline():
    url = database_settings.full_url_sync
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connectable) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine: Engine = create_engine(database_settings.full_url_sync, echo=True)
    with engine.connect() as connection:
        do_run_migrations(connection)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()