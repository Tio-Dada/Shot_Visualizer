# Imports
from nba_api.stats.static import players
from nba_api.stats.endpoints import ShotChartDetail
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
import pandas as pd

def get_player_shot_data(pname,season):
    player = players.find_players_by_full_name(pname) 
    if not player:
        print(f"No player found with the name: {pname}")
        return None
    
    player_id = player[0]['id']
    #all_seasons = PlayerCareerStats(player_id=player_id).get_data_frames()[0]['SEASON_ID'].tolist()
    #print(f"Dictionary for {pname}: {player}") # Returns player information as a list of dictionaries
    #print(f"Player ID for {pname}: {player_id}") # Returns the player ID for the given player name
    #print(f"Seasons for {pname}: {all_seasons}") # Returns all years for the given player name

    """ Shot Chart Detail Endpoint """
    shot_chart_detail = ShotChartDetail(team_id=0, 
                                   player_id=player_id, 
                                   season_nullable=season, 
                                   season_type_all_star='Regular Season',
                                   context_measure_simple='FGA')

    shot_chart_df = shot_chart_detail.get_data_frames()[0]
    print(f"Shot Chart DataFrame for {pname} in {season} Regular Season:")
    num_shots = shot_chart_df.shape[0]
    print(f"Number of shots for {pname} in {season} Regular Season: {num_shots}")
    print(shot_chart_df[['LOC_X', 'LOC_Y', 'SHOT_ATTEMPTED_FLAG', 'SHOT_MADE_FLAG']].head())  # Display the first few rows of the DataFrame

    return shot_chart_df
#get_player_shot_data("Stephen Curry", "2022-23")