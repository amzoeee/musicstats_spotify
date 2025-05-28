import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

n = 10
labels = True # whether or not the labels are shown w track name

plt.rcParams['font.family'] = ['Heiti TC'] # choose font that includes non latin characters

totaldata = pd.read_csv("data/artists.csv") 

totaldata = totaldata.sort_values("times_played", ascending=False)

partial = totaldata.iloc[:n]

fig, ax = plt.subplots()

x = np.arange(0, n)
y = partial['times_played'].tolist()
names = [artist['artist_name'] + '\nplayed ' + str(artist['times_played']) + ' times' for n, artist in partial.iterrows()]


sc = ax.scatter(x, y)

ax.set_ylabel('playcount')
yticks = np.arange((min(y))//500*500, (max(y)) + 20, 500)
ax.set_yticks(ticks=[t for t in yticks], labels=yticks) # scuffed labels
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