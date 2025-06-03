import os
import sys
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from lib.models import Session, Player, Stat, BootColor, Team


def add_player_func():
    """Adds a football player to the database."""
    session = Session()
    try:
        name = input("Enter player name: ").strip()
        player = Player(name=name) 
        session.add(player)
        session.commit()
        print(f"Added player: {name}")
    except ValueError as e:
        print(f"Error: {e}")
    except IntegrityError:
        print("Error: Player with this name already exists. Please use a unique name.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def add_team_func():
    """Adds a football team to the database."""
    session = Session()
    try:
        name = input("Enter team name: ").strip()
        team = Team(name=name) 
        session.add(team)
        session.commit()
        print(f"Added team: {name}")
    except ValueError as e:
        print(f"Error: {e}")
    except IntegrityError:
        print("Error: Team with this name already exists. Please use a unique name.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def add_player_to_team_func():
    """Adds an existing player to an existing team."""
    session = Session()
    try:
        player_id = int(input("Enter player ID: "))
        team_id = int(input("Enter team ID: "))

        player = session.query(Player).get(player_id)
        team = session.query(Team).get(team_id)

        if not player or not team:
            print("Error: Player or team not found. Please check IDs.")
            return

        if team in player.teams:
            print(f"Error: {player.name} is already in {team.name}.")
            return

        player.teams.append(team)
        session.commit()
        print(f"Added {player.name} to {team.name}")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def add_stat_func():
    """Adds stats for a player."""
    session = Session()
    try:
        player_id = int(input("Enter player ID: "))
        goals = int(input("Enter goals: "))
        assists = int(input("Enter assists: "))

        player = session.query(Player).get(player_id)
        if not player:
            print("Error: Player not found.")
            return

        stat = Stat(player_id=player_id, goals=goals, assists=assists) # Validation handled in Stat's __init__
        session.add(stat)
        session.commit()
        print(f"Added stat for {player.name}: {goals} goals, {assists} assists")
    except ValueError as e:
        print(f"Error: {e}. Please enter non-negative numbers for goals/assists and a valid player ID.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def add_boot_color_func():
    """Adds a boot color for a player."""
    session = Session()
    try:
        player_id = int(input("Enter player ID: "))
        
        player = session.query(Player).get(player_id)
        if not player:
            print("Error: Player not found.")
            return

        if player.boot_color:
            print(f"Error: {player.name} already has boot color {player.boot_color.color}.")
            print("To change it, you would need an update feature (not implemented in this menu).")
            return
        
        valid_colors = ["Gold", "Blue", "Red", "White", "Black"]
        color = input(f"Enter boot color ({', '.join(valid_colors)}): ").strip()

        boot_color = BootColor(player_id=player_id, color=color) 
        session.add(boot_color)
        session.commit()
        print(f"Added boot color {color} for {player.name}")
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid player ID and color.")
        session.rollback()
    except IntegrityError:
        print("Error: A unique boot color already exists for this player (or player ID is invalid).")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def list_player_stats_func():
    """Lists stats, boot color, and teams for a specific player."""
    session = Session()
    try:
        player_id = int(input("Enter player ID: "))
        player = session.query(Player).get(player_id)
        if not player:
            print("Error: Player not found.")
            return
        
        stats = player.stats
        total_goals = sum(s.goals for s in stats)
        total_assists = sum(s.assists for s in stats)
        
        boot_color_info = player.boot_color.color if player.boot_color else "None"
        teams = [t.name for t in player.teams] if player.teams else ["None"]
        
        print(f"\n--- Details for {player.name} ---")
        print(f"  Total Goals: {total_goals}")
        print(f"  Total Assists: {total_assists}")
        print(f"  Boot Color: {boot_color_info}")
        print(f"  Teams: {', '.join(teams)}")
        print("-------------------------------")
    except ValueError:
        print("Error: Invalid player ID. Please enter a number.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        session.close()

def list_all_boot_colors_func():
    """Lists all player boot colors."""
    session = Session()
    try:
        boot_colors = session.query(BootColor).all()
        if not boot_colors:
            print("No boot colors found.")
            return
        print("\n--- Football Player Boot Colors ---")
        for bc in boot_colors:
            if bc.player: 
                print(f"  {bc.player.name}: {bc.color}")
            else:
                print(f"  Boot Color ID {bc.id}: {bc.color} (Player not found)")
        print("-----------------------------------")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        session.close()

def list_team_players_func():
    """Lists all players in a specific team."""
    session = Session()
    try:
        team_id = int(input("Enter team ID: "))
        team = session.query(Team).get(team_id)
        if not team:
            print("Error: Team not found.")
            return
        players = [p.name for p in team.players]
        if not players:
            print(f"No players found for {team.name}.")
            return
        print(f"\n--- Players in {team.name} ---")
        for player_name in players:
            print(f"  - {player_name}")
        print("------------------------------")
    except ValueError:
        print("Error: Invalid team ID. Please enter a number.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        session.close()

def show_top_scorers_func():
    """Lists the top 3 goal scorers."""
    session = Session()
    try:
        from sqlalchemy.sql import func
        top_scorers_data = (
            session.query(Player.name, func.sum(Stat.goals).label('total_goals'))
            .join(Stat)
            .group_by(Player.id)
            .order_by(func.sum(Stat.goals).desc())
            .limit(3)
            .all()
        )
        if not top_scorers_data:
            print("No top scorers found.")
            return
        print("\n--- Top 3 Goal Scorers ---")
        for name, goals in top_scorers_data:
            print(f"  {name}: {goals} goals")
        print("--------------------------")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        session.close()

def run_custom_sql_func():
    """Runs a custom SQL query."""
    session = Session()
    try:
        query = input("Enter SQL query: ").strip()
        result = session.execute(text(query)).fetchall()
        if not result:
            print("Query returned no results.")
            return
        
        print("\n--- SQL Query Results ---")
        if hasattr(result[0], '_fields'):
            print(" | ".join(str(f) for f in result[0]._fields))
            print("-" * (sum(len(str(f)) for f in result[0]._fields) + (len(result[0]._fields) - 1) * 3))
        
        for row in result:
            print(" | ".join(str(col) for col in row))
        print("-------------------------")
    except Exception as e:
        print(f"Error executing SQL: {e}")
    finally:
        session.close()

def delete_player_func():
    """Deletes a player from the database by ID."""
    session = Session()
    try:
        player_id = int(input("Enter player ID to delete: "))
        player = session.query(Player).get(player_id)

        if not player:
            print("Error: Player not found.")
            return

        confirm = input(f"Are you sure you want to delete player '{player.name}' (ID: {player.id}) and all associated data (stats, boot color, team associations)? (yes/no): ").strip().lower()
        if confirm == 'yes':

            player.teams.clear() # This removes associations in the player_teams table

            session.delete(player)
            session.commit()
            print(f"Deleted player: {player.name}")
        else:
            print("Player deletion cancelled.")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def delete_team_func():
    """Deletes a team from the database by ID."""
    session = Session()
    try:
        team_id = int(input("Enter team ID to delete: "))
        team = session.query(Team).get(team_id)

        if not team:
            print("Error: Team not found.")
            return

        confirm = input(f"Are you sure you want to delete team '{team.name}' (ID: {team.id}) and all its player associations? (yes/no): ").strip().lower()
        if confirm == 'yes':
            # Remove all players from this team's association
            team.players.clear() # This removes associations in the player_teams table

            session.delete(team)
            session.commit()
            print(f"Deleted team: {team.name}")
        else:
            print("Team deletion cancelled.")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def delete_stat_func():
    """Deletes a player's stat entry by ID."""
    session = Session()
    try:
        stat_id = int(input("Enter stat ID to delete: "))
        stat = session.query(Stat).get(stat_id)

        if not stat:
            print("Error: Stat entry not found.")
            return

        confirm = input(f"Are you sure you want to delete stat entry for player ID {stat.player_id} (Goals: {stat.goals}, Assists: {stat.assists})? (yes/no): ").strip().lower()
        if confirm == 'yes':
            session.delete(stat)
            session.commit()
            print(f"Deleted stat entry with ID: {stat_id}")
        else:
            print("Stat deletion cancelled.")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def delete_boot_color_func():
    """Deletes a player's boot color by player ID."""
    session = Session()
    try:
        player_id = int(input("Enter player ID whose boot color you want to delete: "))
        boot_color = session.query(BootColor).filter_by(player_id=player_id).first()

        if not boot_color:
            print(f"Error: No boot color found for player ID {player_id}.")
            return

        confirm = input(f"Are you sure you want to delete boot color '{boot_color.color}' for player ID {player_id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            session.delete(boot_color)
            session.commit()
            print(f"Deleted boot color for player ID: {player_id}")
        else:
            print("Boot color deletion cancelled.")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def remove_player_from_team_func():
    """Removes a player from a specific team."""
    session = Session()
    try:
        player_id = int(input("Enter player ID to remove from a team: "))
        team_id = int(input("Enter team ID to remove the player from: "))

        player = session.query(Player).get(player_id)
        team = session.query(Team).get(team_id)

        if not player or not team:
            print("Error: Player or team not found. Please check IDs.")
            return

        if team not in player.teams:
            print(f"Error: {player.name} is not currently in {team.name}.")
            return

        player.teams.remove(team)
        session.commit()
        print(f"Removed {player.name} from {team.name}")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

# --- Main Menu Loop ---

# Modify your display_main_menu function in lib/cli.py

def display_main_menu():
    """Displays the interactive menu and handles user choices."""
    while True:
        print("\n--- Football Player Stats CLI Menu ---")
        print("1. Add Player")
        print("2. Add Team")
        print("3. Add Player to Team")
        print("4. Add Player Stats")
        print("5. Add Player Boot Color")
        print("6. List Player Stats (by ID)")
        print("7. List Players in Team (by ID)")
        print("8. List All Boot Colors")
        print("9. Show Top Scorers")
        # print("10. Run Custom SQL Query")
        print("--- Delete Options ---") # New section for clarity
        print("11. Delete Player (by ID)")
        print("12. Delete Team (by ID)")
        print("13. Delete Stat Entry (by ID)")
        print("14. Delete Boot Color (by Player ID)")
        print("15. Remove Player From Team") # New option for many-to-many relationship
        print("0. Exit")
        print("------------------------------------")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_player_func()
        elif choice == '2':
            add_team_func()
        elif choice == '3':
            add_player_to_team_func()
        elif choice == '4':
            add_stat_func()
        elif choice == '5':
            add_boot_color_func()
        elif choice == '6':
            list_player_stats_func()
        elif choice == '7':
            list_team_players_func()
        elif choice == '8':
            list_all_boot_colors_func()
        elif choice == '9':
            show_top_scorers_func()
        elif choice == '10':
            run_custom_sql_func()
        elif choice == '11': # New case for deleting player
            delete_player_func()
        elif choice == '12': # New case for deleting team
            delete_team_func()
        elif choice == '13': # New case for deleting stat
            delete_stat_func()
        elif choice == '14': # New case for deleting boot color
            delete_boot_color_func()
        elif choice == '15': # New case for removing player from team
            remove_player_from_team_func()
        elif choice == '0':
            print("Exiting CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Script Entry Point ---
if __name__ == '__main__':
    display_main_menu()

# Add these functions to lib/cli.py alongside your existing functions

