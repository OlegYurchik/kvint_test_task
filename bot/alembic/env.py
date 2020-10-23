from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

from database.models import db as target_metadata
from utils import generate_dsn
from settings import current_settings


def run_migrations_offline(url: str):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(url: str):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def main():
    config = context.config
    fileConfig(config.config_file_name)

    dsn = generate_dsn(
        engine=current_settings.database.engine,
        host=current_settings.database.host,
        username=current_settings.database.user,
        password=current_settings.database.password,
        name=current_settings.database.name,
        **current_settings.database.params if current_settings.database.paramse else {},
    )

    if context.is_offline_mode():
        run_migrations_offline(dsn)
    else:
        run_migrations_online(dsn)


main()
