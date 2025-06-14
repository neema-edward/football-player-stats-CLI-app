from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Stat(Base):
    """Represents a player's performance stats."""
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    player_id = Column(Integer, ForeignKey('players.id'))

    player = relationship("Player", back_populates="stats")

    def __init__(self, player_id, goals=0, assists=0):
        self.validate_stats(goals, assists) 
        self.player_id = player_id
        self.goals = goals
        self.assists = assists

    def __repr__(self):
        return f"<Stat(goals={self.goals}, assists={self.assists})>"

    def validate_stats(self, goals, assists): 
        """Validate goals and assists."""
        if not isinstance(goals, int) or goals < 0:
            raise ValueError("Goals must be a non-negative integer")
        if not isinstance(assists, int) or assists < 0:
            raise ValueError("Assists must be a non-negative integer")