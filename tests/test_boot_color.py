import pytest
from lib.models import Session, Player, BootColor
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

def test_add_boot_color(setup_db):
    session = setup_db
    player = Player(name="Lionel Messi")
    session.add(player)
    session.commit()
    boot_color = BootColor(player_id=player.id, color="White")
    session.add(boot_color)
    session.commit()
    assert player.boot_color.color == "White"

def test_invalid_boot_color(setup_db):
    session = setup_db
    player = Player(name="Lionel Messi")
    session.add(player)
    session.commit()
    with pytest.raises(ValueError):
        BootColor(player_id=player.id, color="Green")