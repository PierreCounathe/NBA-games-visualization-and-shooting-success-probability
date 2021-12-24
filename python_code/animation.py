import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import matplotlib.image as mpimg
from numpy.core.numeric import full
import pandas as pd
import matplotlib as mpl 
mpl.rcParams['animation.ffmpeg_path'] = '/Users/Pierrecounathe/Downloads/ffmpeg'

image = mpimg.imread("../raw_data/court.png")

size = np.shape(image)
reshape_size = [size[0]/50, size[1]/95]

full_data = pd.read_csv('../modified_data/gamedataset.csv')


fig, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1, figsize = (7, 7), gridspec_kw={'height_ratios': [1, 3]})

ball = full_data[['ball_x', 'ball_y']].iloc[0]
ball_size = full_data['ball_z'].iloc[0]
ball_size_multiplicator = 10
home_players_columns = [f'player_h{i}x' for i in range(1, 6)] + [f'player_h{i}y' for i in range(1, 6)]
home_players = full_data[home_players_columns].iloc[0]
away_players_columns = [f'player_a{i}x' for i in range(1, 6)] + [f'player_a{i}y' for i in range(1, 6)]
away_players = full_data[away_players_columns].iloc[0]

players_jerseys_columns = [f'player_a{i}_jersey' for i in range(1, 6)] + [f'player_h{i}_jersey' for i in range(1, 6)]
players_jerseys = full_data[players_jerseys_columns].iloc[0]

closest_def = full_data['closest_def'].iloc[0]
closest_def_position = full_data[[f'player_a{closest_def}x'] + [f'player_a{closest_def}y']].iloc[0]

ball_carrier = full_data['ball_carrier'].iloc[0]
ball_carrier_position = full_data[[f'player_h{ball_carrier}x'] + [f'player_h{ball_carrier}y']].iloc[0]

ax2.set_ylim(0, size[0])
ax2.set_xlim(0, size[1])

ball_position = [ball[0]*reshape_size[1], ball[1]*reshape_size[0]]
home_team_positions = [home_players[:5]*reshape_size[1], home_players[5:]*reshape_size[0]]
away_team_positions = [away_players[:5]*reshape_size[1], away_players[5:]*reshape_size[0]]

x = list(home_team_positions[0]) + list(away_team_positions[0])
y = list(home_team_positions[1]) + list(away_team_positions[1])

s = 150
c = ['r']*5 + ['blue']*5
scat0 = ax2.scatter(list([ball_position[0]]), list([ball_position[1]]) , s = 30, c = 'orange') #ball
scat1 = ax2.scatter(x, y, s, c, marker = 'o') #10 players

attacking_team = full_data['attack_team'].iloc[0]
if attacking_team == 0:
    scat2 = ax2.scatter([closest_def_position[0]*reshape_size[1]], [closest_def_position[1]*reshape_size[0]], s = 150, facecolors='none', edgecolors='cyan', marker = 'o', label = '                        ', linewidth = 1.5) #square around closest defender
    scat3 = ax2.scatter([ball_carrier_position[0]*reshape_size[1]], [ball_carrier_position[1]*reshape_size[0]], s = 150, facecolors='none', edgecolors='orange', marker = 'o', label = '                        ', linewidth = 2) #square around ball carrier
else:
    scat2 = ax2.scatter([closest_def_position[0]*reshape_size[1]], [closest_def_position[1]*reshape_size[0]], s = 150, facecolors='none', edgecolors='orange', marker = 'o', label = '                        ', linewidth = 1.5) #square around closest defender
    scat3 = ax2.scatter([ball_carrier_position[0]*reshape_size[1]], [ball_carrier_position[1]*reshape_size[0]], s = 150, facecolors='none', edgecolors='cyan', marker = 'o', label = '                        ', linewidth = 2) #square around ball carrier
ax2.set_xticklabels([])
ax2.set_yticklabels([])
ax2.set_xticks([])
ax2.set_yticks([])
ax2.legend()

if attacking_team == 0: # home team attacks
    home_proba_y = [0]
    home_proba_values = [full_data['shoot_prob'].iloc[0]]
    home_proba_line, = ax1.plot(home_proba_y, home_proba_values, color = 'red', markerfacecolor='none')
    away_proba_y = []
    away_proba_values = []
    away_proba_line, = ax1.plot(away_proba_y, away_proba_values, color = 'blue', markerfacecolor='none')
else: # away team attacks
    home_proba_y = []
    home_proba_values = []
    home_proba_line, = ax1.plot(home_proba_y, home_proba_values, color = 'red', markerfacecolor='none')
    away_proba_y = [0]
    away_proba_values = [full_data['shoot_prob'].iloc[0]]
    away_proba_line, = ax1.plot(away_proba_y, away_proba_values, color = 'blue', markerfacecolor='none')

pass_times = []
proba_at_pass_times = []
pass_label, = ax1.plot(pass_times, proba_at_pass_times, '^', label = 'pass marker', color='green', markerfacecolor='none')

ax1.set_xlim(0, 1000)
ax1.set_ylim(0, 1)
ax1.set_xlabel('time in the play')
ax1.set_ylabel('shoot sucess probability')
#ax1.set_xticklabels([str(0.16*l) + 's' for l in range(0, 50, 10)], minor = False)
#ax1.set_xticks(np.arange(0, 50, 10))
ax1.legend()

texts = [ax2.text(0.77, 0.915-i*0.07, '', transform=ax2.transAxes, zorder = 100) for i in range(2)]
annotations = [ax2.annotate(players_jerseys[player], xy=[0, 0], color='w',
                                   horizontalalignment='center',
                                   verticalalignment='center', fontsize = 7, fontweight = 'bold')
                       for player in range(10)]

def animation_frame(i):
    action_number = full_data['action'].iloc[i]
    frame_number = full_data['frame'].iloc[i]
    plt.title(f'play number {action_number}', y = 1.8)

    first_frame_index = full_data[full_data.action == action_number][full_data[full_data.action == action_number].frame == 0].index[0]

    attacking_team = full_data['attack_team'].iloc[i]

    ball = full_data[['ball_x', 'ball_y']].iloc[i]
    ball_size = full_data['ball_z'].iloc[i]

    home_players_columns = [f'player_h{i}x' for i in range(1, 6)] + [f'player_h{i}y' for i in range(1, 6)]
    home_players = full_data[home_players_columns].iloc[i]

    away_players_columns = [f'player_a{i}x' for i in range(1, 6)] + [f'player_a{i}y' for i in range(1, 6)]
    away_players = full_data[away_players_columns].iloc[i]

    closest_def = full_data['closest_def'].iloc[i]
    ball_carrier = full_data['ball_carrier'].iloc[i]

    if attacking_team == 0: # if home team attacks
        closest_def_position = full_data[[f'player_a{closest_def}x'] + [f'player_a{closest_def}y']].iloc[i]
        ball_carrier_position = full_data[[f'player_h{ball_carrier}x'] + [f'player_h{ball_carrier}y']].iloc[i]
        scat2.set_edgecolor('cyan')
        scat3.set_edgecolor('orange')
        texts[0].set_text('closest defender')
        texts[1].set_text('ball carrier')
    else: # if away team attacks
        closest_def_position = full_data[[f'player_h{closest_def}x'] + [f'player_h{closest_def}y']].iloc[i]
        ball_carrier_position = full_data[[f'player_a{ball_carrier}x'] + [f'player_a{ball_carrier}y']].iloc[i]
        scat2.set_edgecolor('orange')
        scat3.set_edgecolor('cyan')
        texts[1].set_text('ball carrier')
        texts[0].set_text('closest defender')
    legend = ax2.legend(loc = 'upper right')

    ax2.set_ylim(0, size[0])
    ax2.set_xlim(0, size[1])

    ball_position = [ball[0]*reshape_size[1], ball[1]*reshape_size[0]]
    home_team_positions = [home_players[:5]*reshape_size[1], home_players[5:]*reshape_size[0]]
    away_team_positions = [away_players[:5]*reshape_size[1], away_players[5:]*reshape_size[0]]

    x = list(home_team_positions[0]) + list(away_team_positions[0])
    y = list(home_team_positions[1]) + list(away_team_positions[1])

    players_jerseys_columns = [f'player_a{i}_jersey' for i in range(1, 6)] + [f'player_h{i}_jersey' for i in range(1, 6)]
    players_jerseys = full_data[players_jerseys_columns].iloc[i]

    scat0.set_sizes([(ball_size + 1)*ball_size_multiplicator]) # ball size
    scat0.set_offsets([ball_position[0], ball_position[1]]) # ball position
    scat1.set_offsets([[x[k], y[k]] for k in range(10)]) # ten players positions
    scat2.set_offsets([closest_def_position[0]*reshape_size[1], closest_def_position[1]*reshape_size[0]]) #closest def
    scat3.set_offsets([ball_carrier_position[0]*reshape_size[1], ball_carrier_position[1]*reshape_size[0]]) #ball_carrier

    sub_data = full_data[full_data.action == action_number]
    sub_sub_data = sub_data[sub_data.frame <= frame_number]
    home_proba_y = list(sub_sub_data[sub_sub_data.attack_team == 0].frame)
    away_proba_y = list(sub_sub_data[sub_sub_data.attack_team == 1].frame)
    home_proba_values = list(sub_sub_data[sub_sub_data.attack_team == 0].shoot_prob)
    away_proba_values = list(sub_sub_data[sub_sub_data.attack_team == 1].shoot_prob)
    home_proba_line.set_data(home_proba_y, home_proba_values)
    away_proba_line.set_data(away_proba_y, away_proba_values)

    pass_times = [l - first_frame_index for l in range(first_frame_index, first_frame_index+frame_number+1) if full_data['pass'].iloc[l] == 1]
    proba_at_pass_times = [full_data['shoot_prob'].iloc[l] for l in pass_times]
    pass_label.set_data(pass_times, proba_at_pass_times)

    for k in range(10):
        annotations[k].set_position((x[k], y[k]))
        annotations[k].set_text(players_jerseys[k])

    return scat0, scat1, scat2, scat3, home_proba_line, away_proba_line, pass_label, legend

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

def animate_play_number(play_number = None, filename = None):
    if play_number == None:
        anim = animation.FuncAnimation(fig, func = animation_frame, frames = np.arange(0, 10000+1, 2), interval = 10)
        ax2.imshow(image)
        plt.show()
    else:
        first_frame_index = full_data[full_data.action == play_number].index[0]
        last_frame_index = full_data[full_data.action == play_number].index[-1]
        anim = animation.FuncAnimation(fig, func = animation_frame, frames = np.arange(first_frame_index, last_frame_index+1, 2), interval = 10)
        ax2.imshow(image)
        plt.show()
    if filename!= None:
        # save the animation
        anim.save(filename ,writer = writer)

""" anim = animation.FuncAnimation(fig, func = animation_frame, frames = np.arange(0, 1999+1, 2), interval = 1)

ax2.imshow(image)
plt.show() """

# Use the function below to run the animation on a single play
# The parameter is the play number, called 'action' in the dataframe
# put a filename as a parameter to save the gif
animate_play_number(59, '../results/example.gif')
#animate_play_number(59)