from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.models import Base, player_teams

class Team(Base):
    """Represents a football team."""
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    players = relationship("Player", secondary=player_teams, back_populates="teams")

    def __repr__(self):
        return f"<Team(name={self.name})>"

    def validate_name(self, name):
        """Validate team name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")