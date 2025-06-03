from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base 
from .player_team import player_teams 

class Player(Base):
    """Represents a football player."""
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    stats = relationship("Stat", back_populates="player")
    boot_color = relationship("BootColor", uselist=False, back_populates="player")
    teams = relationship("Team", secondary=player_teams, back_populates="players")

    def __init__(self, name):
        self.validate_name(name) 
        self.name = name

    def __repr__(self):
        return f"<Player(name={self.name})>"

    def validate_name(self, name): 
        """Validate player name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")