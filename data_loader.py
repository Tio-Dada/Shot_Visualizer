# Imports
from nba_api.stats.static import players
from nba_api.stats.endpoints import ShotChartDetail
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
import pandas as pd

# Browser headers to prevent cloud IP blocking by NBA stats firewall
CUSTOM_HEADERS = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive',
}

def get_player_seasons(pname):
    player = players.find_players_by_full_name(pname)
    if not player:
        return None
    
    player_id = player[0]['id']
    try:
        career = PlayerCareerStats(
            player_id=player_id,
            headers=CUSTOM_HEADERS,
            timeout=60
        )
        df = career.get_data_frames()[0]
        # Return unique seasons sorted descending (newest first)
        seasons = sorted(df['SEASON_ID'].unique().tolist(), reverse=True)
        return seasons
    except Exception as e:
        print(f"Error fetching seasons for {pname}: {e}")
        return None

def get_player_shot_data(pname, season):
    player = players.find_players_by_full_name(pname)
    if not player:
        return None
    
    player_id = player[0]['id']
    try:
        shot_chart_detail = ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable=season,
            season_type_all_star='Regular Season',
            context_measure_simple='FGA',
            headers=CUSTOM_HEADERS,
            timeout=60
        )
        shot_chart_df = shot_chart_detail.get_data_frames()[0]
        return shot_chart_df
    except Exception as e:
        print(f"Error fetching shot data for {pname} in {season}: {e}")
        return None