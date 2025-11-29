import pandas as pd
import matplotlib.pyplot as plt
import os
from colorsys import hsv_to_rgb
import textwrap

plt.rcParams['font.family'] = ['Heiti TC']

def get_color(artist):
    """Generate consistent color for artist based on hash"""
    h = hash(artist)
    hue = (h % 360) / 360.0
    saturation = 0.6 + ((h // 360) % 40) / 100.0
    value = 0.8 + ((h // 36000) % 20) / 100.0
    return hsv_to_rgb(hue, saturation, value)

# Load data
jsons = []
directory = 'rawdata'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and str(filename)[0] != ".":
        jsons.append(str(f))

cleaneddata = []

for jsonpath in jsons:
    if jsonpath.split(".")[-1] != "json":
        continue
    data = pd.read_json(jsonpath)
    cleaneddata.append(data[["master_metadata_album_artist_name", 
                             "master_metadata_track_name",
                             "ms_played"]])
totaldata = pd.concat(cleaneddata)

# Filter out None values
totaldata = totaldata.dropna(subset=['master_metadata_track_name', 'master_metadata_album_artist_name'])

# Top stats by playtime
top_n = 15

top_artists = totaldata.groupby('master_metadata_album_artist_name')['ms_played'].sum() / (1000 * 60 * 60)
top_artists = top_artists.nlargest(top_n)
top_tracks_grouped = totaldata.groupby(totaldata['master_metadata_album_artist_name'] + " - " + 
                                       totaldata['master_metadata_track_name'])['ms_played'].sum() / (1000 * 60 * 60)
top_tracks_grouped = top_tracks_grouped.nlargest(top_n)

fig_stats, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Top artists bar chart
artist_colors = [get_color(artist) for artist in top_artists.index]
top_artists.plot(kind='barh', ax=ax1, color=artist_colors)
ax1.set_xlabel('total playtime (hours)')
ax1.set_ylabel('')
ax1.set_title(f'top {top_n} artists by playtime')
ax1.invert_yaxis()

# Top tracks bar chart
track_colors = [get_color(track.split(" - ")[0]) for track in top_tracks_grouped.index]
top_tracks_grouped.plot(kind='barh', ax=ax2, color=track_colors)
ax2.set_xlabel('total playtime (hours)')
ax2.set_ylabel('')
ax2.set_title(f'top {top_n} tracks by playtime')
ax2.invert_yaxis()

# Wrap long track names
wrapped_labels = ['\n'.join(textwrap.wrap(label.get_text(), width=30)) 
                  for label in ax2.get_yticklabels()]
ax2.set_yticklabels(wrapped_labels, fontsize=9)

plt.tight_layout()
plt.show()
