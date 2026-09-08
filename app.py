import streamlit as st
from court import draw_court
import data_loader as dl
import matplotlib.pyplot as plt

st.set_page_config(page_title="NBA Shot Visualizer", layout="wide")
# Set up the sidebar for user inputs
st.sidebar.header("Player Shot Chart Settings")
player_name = st.sidebar.text_input("Player Name", value="Stephen Curry", key="player_name")
player = dl.players.find_players_by_full_name(player_name)
if player:
    player_id = player[0]['id']
    season_options = dl.PlayerCareerStats(player_id=player_id).get_data_frames()[0]['SEASON_ID'].tolist()
else:
    season_options = []

season = st.sidebar.selectbox("Season", options=season_options, key="season")
shot_types = st.sidebar.radio("Shot Type", options=['All Shots', '2PT Field Goal', '3PT Field Goal'], key="shot_types")
Visualizer = st.sidebar.radio("Visualize Shot Chart", options=['Scatter (Makes & Misses)', 'Hexbin Density (Frequency)'], key="visualize_button")

@st.cache_data
def fetch_shot_data(player_name, season):
    return dl.get_player_shot_data(player_name, season)


shot_data = fetch_shot_data(player_name, season)
if shot_data is None:
    st.warning(f"No shot data found for {player_name} in {season}. Please check the player name and season.")
    st.stop()

# Filter shot data based on selected shot type
if shot_types == '2PT Field Goal':
    shot_data = shot_data[shot_data['SHOT_TYPE'] == '2PT Field Goal']
elif shot_types == '3PT Field Goal':
    shot_data = shot_data[shot_data['SHOT_TYPE'] == '3PT Field Goal']
elif shot_types == 'All Shots':
    pass  # No filtering needed for all shots
shot_attempts = shot_data.shape[0]
shot_made = shot_data[shot_data['SHOT_MADE_FLAG'] == 1].shape[0]
shot_missed = shot_attempts - shot_made
fg_percentage = (shot_made / shot_attempts * 100) if shot_attempts > 0 else 0



col1, col2, col3 = st.columns(3)
col1.metric("Total Shots Attempted", shot_attempts)
col2.metric("Total Shots Made", shot_made)
col3.metric("Field Goal Percentage", f"{fg_percentage:.1f}%")

fig, ax = plt.subplots(figsize=(12, 11))
draw_court(ax=ax)
if Visualizer == 'Scatter (Makes & Misses)':
    ax.scatter(shot_data[shot_data['SHOT_MADE_FLAG'] == 0]['LOC_X'], shot_data[shot_data['SHOT_MADE_FLAG'] == 0]['LOC_Y'], marker='x', color='red', s=50, alpha=0.7, label='Misses')
    ax.scatter(shot_data[shot_data['SHOT_MADE_FLAG'] == 1]['LOC_X'], shot_data[shot_data['SHOT_MADE_FLAG'] == 1]['LOC_Y'], marker='o', color='green', s=50, alpha=0.7, label='Makes')
elif Visualizer == 'Hexbin Density (Frequency)':
    representation = ax.hexbin(shot_data['LOC_X'], shot_data['LOC_Y'], 
                               gridsize=(28, 28), cmap='YlOrRd', mincnt=1, 
                               extent=(-250, 250, -47.5, 422.5), alpha=0.74,
                               edgecolors='none', zorder=2, bins='log')
    plt.colorbar(representation, ax=ax, label='Shot Frequency')
ax.set_title(f"{player_name} Shot Chart - {season}")
st.pyplot(fig)
