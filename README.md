Football Player Stats CLI
A CLI to manage football players, their stats, boot colors, and team affiliations. Track any players and teams, such as Lionel Messi at Barcelona or Cristiano Ronaldo at Manchester United.
User Stories

As a football fan, I want to add a new player to track stars like Neymar.
As a football fan, I want to add goals for a player to see their scoring record.
As a football fan, I want to see all players’ boot colors to know who wears white boots.
As a football fan, I want to assign players to teams to track club rosters.

Setup

Install dependencies: pipenv install
Activate environment: pipenv shell
Initialize database: alembic upgrade head
Run CLI: python lib/cli.py
Run tests: pytest

CLI Commands

add-player <name>: Add a football player.
add-team <name>: Add a football team.
add-player-to-team <player_id> <team_id>: Add a player to a team.
add-stat <player_id> <goals> <assists>: Add a stat for a player.
add-boot-color <player_id> <color>: Add a boot color (Gold, Blue, Red, White, Black).
list-player-stats <player_id>: List stats, boot color, and teams for a player.
list-boot-colors: List all player boot colors.
list-team-players <team_id>: List all players in a team.
top-scorers: List top 3 goal scorers.
run-sql <query>: Run a custom SQL query.



