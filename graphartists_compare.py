import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

n = 1000

labels = True

plt.rcParams['font.family'] = ['Heiti TC'] # choose font that includes non latin characters

totaldata = pd.read_csv("data/artists.csv")

partial = totaldata.iloc[:n]

fig, ax = plt.subplots()

ax.set_xlabel('unique tracks')
ax.set_ylabel('playcount')

x = partial['unique_tracks'].tolist()
y = partial['times_played'].tolist()
artist_names = partial['artist_name'].tolist()

ax.set_xlabel('unique tracks')
xticks = np.arange((min(x))//10*10, (max(x)) + 1, 10)
ax.set_xticks(ticks=[t for t in xticks], labels=xticks) # scuffed labels
ax.set_ylabel('playcount')
yticks = np.arange((min(y))//500*500, (max(y)) + 20, 500)
ax.set_yticks(ticks=[t for t in yticks], labels=yticks) # scuffed labels

sc = ax.scatter(x, y)

if labels:
    annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

def update_annot(ind):
    n = ind["ind"][0]

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}\nunique tracks: {}\nplaycount: {}".format(artist_names[n], x[n], y[n])
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