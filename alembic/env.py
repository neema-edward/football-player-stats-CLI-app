import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models import Base, player_teams
from sqlalchemy import create_engine
from alembic import context

config = context.config
connectable = create_engine(config.get_main_option("sqlalchemy.url"))
with connectable.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=Base.metadata
    )
    with context.begin_transaction():
        context.run_migrations()