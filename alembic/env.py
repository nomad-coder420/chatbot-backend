from alembic import context
from sqlalchemy import create_engine
from logging.config import fileConfig

from chatbot.core.constants import SYNC_DATABASE_URL
from chatbot.core.models import Base

import chatbot.components.user.models
import chatbot.components.auth.models
import chatbot.components.chat.models

config = context.config
target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")

    if not url:
        raise Exception("No database URL found")

    engine = create_engine(url)

    context.configure(
        connection=engine.connect(),
        url=url,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


run_migrations()
