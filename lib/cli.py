import click
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from lib.models import Session, Player, Stat, BootColor, Team

@click.group()
def cli():
    """Football Player Stats CLI."""
    pass

@cli.command()
@click.argument('name')
def add_player(name):
    """Add a football player."""
    session = Session()
    try:
        Player.validate_name(None, name)
        player = Player(name=name)
        session.add(player)
        session.commit()
        click.echo(f"Added player: {name}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except IntegrityError:
        click.echo("Error: Player already exists")
        session.rollback()
    finally:
        session.close()

@cli.command()
@click.argument('name')
def add_team(name):
    """Add a football team."""
    session = Session()
    try:
        Team.validate_name(None, name)
        team = Team(name=name)
        session.add(team)
        session.commit()
        click.echo(f"Added team: {name}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except IntegrityError:
        click.echo("Error: Team already exists")
        session.rollback()
    finally:
        session.close()

@cli.command()
@click.argument('player_id', type=int)
@click.argument('team_id', type=int)
def add_player_to_team(player_id, team_id):
    """Add a player to a team."""
    session = Session()
    try:
        player = session.query(Player).get(player_id)
        team = session.query(Team).get(team_id)
        if not player or not team:
            click.echo("Error: Player or team not found")
            return
        player.teams.append(team)
        session.commit()
        click.echo(f"Added {player.name} to {team.name}")
    except IntegrityError:
        click.echo("Error: Player is already in this team")
        session.rollback()
    finally:
        session.close()

@cli.command()
@click.argument('player_id', type=int)
@click.argument('goals', type=int)
@click.argument('assists', type=int)
def add_stat(player_id, goals, assists):
    """Add stats for a player."""
    session = Session()
    try:
        player = session.query(Player).get(player_id)
        if not player:
            click.echo("Error: Player not found")
            return
        Stat.validate_stats(None, goals, assists)
        stat = Stat(player_id=player_id, goals=goals, assists=assists)
        session.add(stat)
        session.commit()
        click.echo(f"Added stat for {player.name}: {goals} goals, {assists} assists")
    except ValueError as e:
        click.echo(f"Error: {e}")
    finally:
        session.close()

@cli.command()
@click.argument('player_id', type=int)
@click.argument('color')
def add_boot_color(player_id, color):
    """Add a boot color for a player."""
    session = Session()
    try:
        player = session.query(Player).get(player_id)
        if not player:
            click.echo("Error: Player not found")
            return
        BootColor.validate_color(None, color)
        boot_color = BootColor(player_id=player_id, color=color)
        session.add(boot_color)
        session.commit()
        click.echo(f"Added boot color {color} for {player.name}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except IntegrityError:
        click.echo("Error: Player already has a boot color")
        session.rollback()
    finally:
        session.close()

@cli.command()
@click.argument('player_id', type=int)
def list_player_stats(player_id):
    """List stats, boot color, and teams for a player."""
    session = Session()
    try:
        player = session.query(Player).get(player_id)
        if not player:
            click.echo("Error: Player not found")
            return
        stats = player.stats
        stat_list = [(s.goals, s.assists) for s in stats]  # Tuple for stats
        total_goals = sum(s[0] for s in stat_list)
        total_assists = sum(s[1] for s in stat_list)
        stats_dict = {"total_goals": total_goals, "total_assists": total_assists}  # Dict for summary
        boot_color = player.boot_color.color if player.boot_color else "None"
        teams = [t.name for t in player.teams]  # List for teams
        click.echo(f"Stats for {player.name}: {stats_dict}, Boot Color: {boot_color}, Teams: {teams}")
    finally:
        session.close()

@cli.command()
def list_boot_colors():
    """List all player boot colors."""
    session = Session()
    try:
        boot_colors = session.query(BootColor).all()
        color_list = [f"{b.player.name}: {b.color}" for b in boot_colors]  # List for output
        click.echo("Football Player Boot Colors:")
        for item in color_list:
            click.echo(item)
    finally:
        session.close()

@cli.command()
@click.argument('team_id', type=int)
def list_team_players(team_id):
    """List all players in a team."""
    session = Session()
    try:
        team = session.query(Team).get(team_id)
        if not team:
            click.echo("Error: Team not found")
            return
        players = [p.name for p in team.players]  # List for players
        click.echo(f"Players in {team.name}: {players}")
    finally:
        session.close()

@cli.command()
def top_scorers():
    """List top 3 goal scorers."""
    session = Session()
    try:
        from sqlalchemy.sql import func
        top_scorers = (
            session.query(Player.name, func.sum(Stat.goals).label('total_goals'))
            .join(Stat)
            .group_by(Player.id)
            .order_by(func.sum(Stat.goals).desc())
            .limit(3)
            .all()
        )
        click.echo("Top 3 Goal Scorers:")
        for name, goals in top_scorers:  # Tuple unpacking
            click.echo(f"{name}: {goals} goals")
    finally:
        session.close()

@cli.command()
@click.argument('query')
def run_sql(query):
    """Run a custom SQL query."""
    session = Session()
    try:
        result = session.execute(text(query)).fetchall()
        for row in result:
            click.echo(row)
    except Exception as e:
        click.echo(f"Error: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    cli()