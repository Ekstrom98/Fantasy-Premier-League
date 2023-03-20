import pickle
# Replace 'file_path.pkl' with the path to your pickle file
file_path = 'players.pickle'

with open(file_path, 'rb') as file:
    data = pickle.load(file)

nbr_of_players = len(data)


player_dict = {}
for i in range(nbr_of_players):
    player_data = data[i].split()
    name = player_data[1] + " " + player_data[2]
    current_player_stats = []

    this_season =data[i].split('This Season')[1]
    if('Totals' in this_season):
        this_season = data[i].split('This Season')[1].split('Totals')[0]
        
        season_stats_categories = this_season.split()[0:29]
        this_season=this_season.split()[29::]#[0:33]
        nbr_of_gws = int(len(this_season)/33)
        for j in range(nbr_of_gws):
            gw_stats = this_season[j*33:(j+1)*33]
            current_player_stats.append(gw_stats)
        player_dict[name] = current_player_stats


        totals = data[i].split('This Season')[1].split('Totals')[1].split('Per 90')[0]
        per_90 = data[i].split('This Season')[1].split('Per 90')[1]

print(data[-1])