import pytest
from lib.models import Session, Player, Team
from sqlalchemy import create_engine
from lib.models import Base

@pytest.fixture
def setup_db():
    engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_add_team(setup_db):
    session = setup_db
    team = Team(name="Barcelona")
    session.add(team)
    session.commit()
    assert team.id is not None
    assert team.name == "Barcelona"

def test_team_players(setup_db):
    session = setup_db
    player = Player(name="Lionel Messi")
    team = Team(name="Barcelona")
    session.add(player)
    session.add(team)
    session.commit()
    player.teams.append(team)
    session.commit()
    assert len(team.players) == 1
    assert team.players[0].name == "Lionel Messi"

def test_invalid_team_name(setup_db):
    with pytest.raises(ValueError):
        Team(name="")