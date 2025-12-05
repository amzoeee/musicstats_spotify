import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hashlib
from colorsys import hsv_to_rgb

n = 1000
labels = True

def convert_ms(ms): # function to convert ms to hr, min, and sec 
    return str((ms//1000)//3600) + " hr, " + str((ms//1000)//60%60) + " min, " + str((ms//1000)%60) + " sec" 

plt.rcParams['font.family'] = ['Heiti TC'] # choose font that includes non latin characters

totaldata = pd.read_csv("data/tracks.csv")

partial = totaldata.iloc[:n]

fig, ax = plt.subplots()
ax.set_title('Track Playcount v. Playtime')


def get_color(artist):
    """Generate consistent color for artist based on hash"""
    h = int(hashlib.md5(artist.encode()).hexdigest(), 16)
    hue = (h % 360) / 360.0
    saturation = 0.6 + ((h // 360) % 40) / 100.0
    value = 0.8 + ((h // 36000) % 20) / 100.0
    return hsv_to_rgb(hue, saturation, value)

x_ms = partial['ms_played'].tolist()
x = [ms / (1000 * 60 * 60) for ms in x_ms]
y = partial['times_played'].tolist()
track_names = partial['track_name'].tolist()
artist_names = partial['artist_name'].tolist()
colors = [get_color(artist) for artist in artist_names]

ax.set_xlabel('Playtime (in hrs)')
# 10 nicely spaced x-ticks with appropriate magnitude
x_min, x_max = min(x), max(x)
x_range = x_max - x_min
magnitude = 10 ** np.floor(np.log10(x_range / 10))
x_step = np.ceil(x_range / 10 / magnitude) * magnitude
x_min_rounded = np.floor(x_min / magnitude) * magnitude
x_max_rounded = np.ceil(x_max / magnitude) * magnitude
xticks = np.arange(x_min_rounded, x_max_rounded + x_step, x_step)
ax.set_xticks(ticks=xticks)
ax.set_ylabel('Playcount')
# 10 nicely spaced y-ticks with appropriate magnitude
y_min, y_max = min(y), max(y)
y_range = y_max - y_min
magnitude = 10 ** np.floor(np.log10(y_range / 10))
y_step = np.ceil(y_range / 10 / magnitude) * magnitude
y_min_rounded = np.floor(y_min / magnitude) * magnitude
y_max_rounded = np.ceil(y_max / magnitude) * magnitude
yticks = np.arange(y_min_rounded, y_max_rounded + y_step, y_step)
ax.set_yticks(ticks=yticks)


sc = ax.scatter(x, y, c=colors)

if labels:
    annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

def update_annot(ind):
    n = ind["ind"][0]

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{} - {}\nplaytime: {}\nplaycount: {}".format(track_names[n], artist_names[n], convert_ms(x_ms[n]), y[n])
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