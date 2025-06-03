from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base 
from .player_team import player_teams 

class Team(Base):
    """Represents a football team."""
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    players = relationship("Player", secondary=player_teams, back_populates="teams")

    def __init__(self, name):
        self.validate_name(name) 
        self.name = name

    def __repr__(self):
        return f"<Team(name={self.name})>"

    def validate_name(self, name): 
        """Validate team name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")