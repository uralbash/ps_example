from __future__ import with_statement

from logging.config import fileConfig

from pyramid_sqlalchemy import BaseObject
from sqlalchemy import engine_from_config, pool

from alembic import context
from ps_example.includes.auth.models import *  # noqa
from ps_example.includes.home.models import *  # noqa
from ps_example.includes.home.models.funny_models import *  # noqa
from ps_example.includes.home.models.postgres import *  # noqa
from ps_example.includes.pages.models import *  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = BaseObject.metadata
exclude_tables = ('alembic_version', )

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in exclude_tables:
        return False
    else:
        return True


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    target_metadata.reflect(engine)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
        try:
            impl = context.get_impl().context_opts['template_args']
            downgrades = impl['downgrades']
            upgrades = impl['upgrades']
            if 'pass' in downgrades and 'pass' in upgrades:
                raise Exception("Empty migration")
        except KeyError:
            pass
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
