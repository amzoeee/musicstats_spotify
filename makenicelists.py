import pandas as pd

def convert_ms(ms): # function to convert ms to hr, min, and sec 
    return str((ms//1000)//3600) + " hr, " + str((ms//1000)//60%60) + " min, " + str((ms//1000)%60) + " sec" 

tracks_playtime = pd.read_csv("data/tracks.csv")
tracks_playcount = tracks_playtime.sort_values("times_played", ascending=False)
artists_playtime = pd.read_csv("data/artists.csv")
artists_playcount = artists_playtime.sort_values("times_played", ascending=False)
artists_uniquetracks = artists_playtime.sort_values("unique_tracks", ascending=False)


file = open("formatteddata/tracks_playtime.txt", "w")
file.write("track stats :D (sorted by playtime)\n")
for index, s in tracks_playtime.iterrows():
    file.write(str(s.get("track_name")) + " - " + str(s.get("artist_name")) + ": " + convert_ms(s.get("ms_played")) + " \n")
file.close()

file = open("formatteddata/tracks_playcount.txt", "w")
file.write("track stats :D (sorted by playcount)\n")
for index, s in tracks_playcount.iterrows():
    file.write(str(s.get("track_name")) + " - " + str(s.get("artist_name")) + ": " + str(s.get("times_played")) + " plays \n")
file.close()


file = open("formatteddata/artists_playtime.txt", "w")
file.write("artist stats :D (sorted by playtime)\n")
for index, s in artists_playtime.iterrows():
    file.write(str(s.get("artist_name"))+ ": " + convert_ms(s.get("ms_played")) + " \n")
file.close()

file = open("formatteddata/artists_playcount.txt", "w")
file.write("artist stats :D (sorted by playcount)\n")
for index, s in artists_playcount.iterrows():
    file.write(str(s.get("artist_name")) + ": " + str(s.get("times_played")) + " plays \n")
file.close()

file = open("formatteddata/artists_uniquetracks.txt", "w")
file.write("artist stats :D (sorted by playcount)\n")
for index, s in artists_uniquetracks.iterrows():
    file.write(str(s.get("artist_name")) + ": " + str(s.get("unique_tracks")) + " tracks \n")
file.close()