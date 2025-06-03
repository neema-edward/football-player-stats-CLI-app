from sqlalchemy import Column, Integer, ForeignKey, Table
from .base import Base


player_teams = Table(
    'player_teams',
    Base.metadata,
    Column('player_id', Integer, ForeignKey('players.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
)