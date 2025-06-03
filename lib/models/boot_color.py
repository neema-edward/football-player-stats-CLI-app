from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class BootColor(Base):
    """Represents a player's boot color."""
    __tablename__ = 'boot_colors'

    id = Column(Integer, primary_key=True)
    color = Column(String, nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), unique=True)

    player = relationship("Player", back_populates="boot_color")

    def __init__(self, player_id, color):
        self.validate_color(color) 
        self.player_id = player_id
        self.color = color

    def __repr__(self):
        return f"<BootColor(color={self.color})>"

    def validate_color(self, color): 
        """Validate boot color."""
        valid_colors = ["Gold", "Blue", "Red", "White", "Black"]
        if color not in valid_colors:
            raise ValueError(f"Color must be one of: {', '.join(valid_colors)}")