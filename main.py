from court import draw_court
import data_loader as dl
import matplotlib.pyplot as plt

# Example usage
player_name = "Stephen Curry"
season = "2022-23"
# Get the player's shot data
shot_data = dl.get_player_shot_data(player_name, season)
# makes and misses dataframe
makes = shot_data[shot_data['SHOT_MADE_FLAG'] == 1]
misses = shot_data[shot_data['SHOT_MADE_FLAG'] == 0]

fig, ax = plt.subplots(figsize=(12, 11))

#draw_court(ax=ax)


ax.scatter(misses['LOC_X'], misses['LOC_Y'], marker='x', color='red', s=50, alpha=0.7)
ax.scatter(makes['LOC_X'], makes['LOC_Y'], marker='o', color='green', s=50, alpha=0.7)

ax.set_title(f"{player_name} Shot Chart - {season}")

#plt.show()