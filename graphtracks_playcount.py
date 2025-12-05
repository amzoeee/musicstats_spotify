import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hashlib
from colorsys import hsv_to_rgb

n = 10
labels = True # whether or not the labels are shown w track name

plt.rcParams['font.family'] = ['Heiti TC'] # choose font that includes non latin characters

totaldata = pd.read_csv("data/tracks.csv")

totaldata = totaldata.sort_values("times_played", ascending=False)

partial = totaldata.iloc[:n]

fig, ax = plt.subplots()

def get_color(artist):
    """Generate consistent color for artist based on hash"""
    h = int(hashlib.md5(artist.encode()).hexdigest(), 16)
    hue = (h % 360) / 360.0
    saturation = 0.6 + ((h // 360) % 40) / 100.0
    value = 0.8 + ((h // 36000) % 20) / 100.0
    return hsv_to_rgb(hue, saturation, value)

x = np.arange(0, n)
y = partial['times_played'].tolist()
names = [track['artist_name'] + " - " + track['track_name'] + '\nplayed ' + str(track['times_played']) + ' times' for n, track in partial.iterrows()]
artist_names = partial['artist_name'].tolist()
colors = [get_color(artist) for artist in artist_names]

sc = ax.scatter(x, y, c=colors)

ax.set_ylabel('playcount')
# 10 nicely spaced y-ticks with appropriate magnitude
y_min, y_max = min(y), max(y)
y_range = y_max - y_min
magnitude = 10 ** np.floor(np.log10(y_range / 10))
y_step = np.ceil(y_range / 10 / magnitude) * magnitude
y_min_rounded = np.floor(y_min / magnitude) * magnitude
y_max_rounded = np.ceil(y_max / magnitude) * magnitude
yticks = np.arange(y_min_rounded, y_max_rounded + y_step, y_step)
ax.set_yticks(ticks=yticks)
ax.set_xticks(ticks=[])


if labels: 

    annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

def update_annot(ind):
    n = ind["ind"][0]

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = names[n]
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()
if labels:
    fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()