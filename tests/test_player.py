import pytest
from lib.models import Session, Player, Stat 
from lib.models.base import Base 
from sqlalchemy import create_engine

@pytest.fixture
def setup_db():
    engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_add_player(setup_db):
    session = setup_db
    player = Player(name="Lionel Messi")
    session.add(player)
    session.commit()
    assert player.id is not None
    assert player.name == "Lionel Messi"

def test_player_stats(setup_db):
    session = setup_db
    player = Player(name="Lionel Messi")
    session.add(player)
    session.commit()
    stat = Stat(player_id=player.id, goals=2, assists=1)
    session.add(stat)
    session.commit()
    assert len(player.stats) == 1
    assert player.stats[0].goals == 2

def test_invalid_player_name(setup_db):
    with pytest.raises(ValueError):
        Player(name="")