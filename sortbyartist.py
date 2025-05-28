import pandas as pd


# takes data from tracks_all.csv
try:
    totaldata = pd.read_csv('data/tracks.csv')
except: 
    print("make sure to run sortbytrack.py first!")
    exit()
aggregation_functions2 = {
                         'track_name' : 'size', # count how many of each track 
                         'times_played' : 'sum', 
                         'ms_played' : 'sum'
                         }

totaldata = totaldata.groupby(totaldata['artist_name']).agg(aggregation_functions2)

totaldata.rename(columns={"track_name" : "unique_tracks"}, inplace=True)

totaldata = totaldata.sort_values("ms_played", ascending=False)

totaldata.to_csv('data/artists.csv')


