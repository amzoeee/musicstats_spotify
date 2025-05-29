import pandas as pd
import os
# import matplotlib.pyplot as plt

jsons = []
# assign directory
directory = 'rawdata'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f) and str(filename)[0] != ".":
        jsons.append(str(f))


cleaneddata = [] # list of all plays of songs w/ ms played, track name, artist name + track uri

for jsonpath in jsons:
    if jsonpath.split(".")[-1] != "json":
        continue
    data = pd.read_json(jsonpath)
    cleaneddata.append(data[["ms_played", 
                             "master_metadata_album_artist_name", 
                             "master_metadata_track_name", 
                             "spotify_track_uri", 
                             "ts"]])
# ts is a temporary column thingy used to count the amt of times the track was played

totaldata = pd.concat(cleaneddata) 

totaldata = totaldata[totaldata["ms_played"] != 0] # clean out the 0s 

totaldata.rename(columns={"master_metadata_album_artist_name" : "artist_name", "master_metadata_track_name" : "track_name"}, inplace=True)

aggregation_functions = {'ms_played': 'sum', 
                         'artist_name' : 'first', 
                         'track_name' : 'first',
                         'ts' : 'size' # ts used to count the amt of times each track was played
                         }

totaldata = totaldata.groupby(totaldata['spotify_track_uri']).agg(aggregation_functions)

totaldata.rename(columns={"ts" : "times_played"}, inplace=True)

totaldata = totaldata.sort_values("ms_played", ascending=False)

totaldata.to_csv('data/tracks.csv')
