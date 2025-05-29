from sqlalchemy import Column, Integer, String, ForeignKey, Table
from alembic import op

def upgrade():
    op.create_table(
        'players',
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False)
    )
    op.create_table(
        'teams',
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False)
    )
    op.create_table(
        'stats',
        Column('id', Integer, primary_key=True),
        Column('goals', Integer, default=0),
        Column('assists', Integer, default=0),
        Column('player_id', Integer, ForeignKey('players.id'))
    )
    op.create_table(
        'boot_colors',
        Column('id', Integer, primary_key=True),
        Column('color', String, nullable=False),
        Column('player_id', Integer, ForeignKey('players.id'), unique=True)
    )
    op.create_table(
        'player_teams',
        Column('player_id', Integer, ForeignKey('players.id'), primary_key=True),
        Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
    )

def downgrade():
    op.drop_table('player_teams')
    op.drop_table('boot_colors')
    op.drop_table('stats')
    op.drop_table('teams')
    op.drop_table('players')