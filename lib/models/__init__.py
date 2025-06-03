# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from .base import Base

# from .player_team import player_teams
# from .player import Player
# from .team import Team
# from .stat import Stat
# from .boot_color import BootColor

# engine = create_engine('sqlite:///football.db')
# # Base = declarative_base()
# Session = sessionmaker(bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base # Correctly import Base from .base
from .player_team import player_teams # Correctly import player_teams from .player_team

# These imports are good, as they define your models and register them with Base.metadata
from .player import Player
from .team import Team
from .stat import Stat
from .boot_color import BootColor

engine = create_engine('sqlite:///football.db')
Session = sessionmaker(bind=engine)

# Base.metadata.create_all(engine) # You usually do this via Alembic migrations