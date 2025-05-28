import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

n = 1000
labels = True

def convert_ms(ms): # function to convert ms to hr, min, and sec 
    return str((ms//1000)//3600) + " hr, " + str((ms//1000)//60%60) + " min, " + str((ms//1000)%60) + " sec" 

plt.rcParams['font.family'] = ['Heiti TC'] # choose font that includes non latin characters

totaldata = pd.read_csv("data/tracks.csv")

partial = totaldata.iloc[:n]

fig, ax = plt.subplots()

x = partial['ms_played'].tolist()
y = partial['times_played'].tolist()
track_names = partial['track_name'].tolist()
artist_names = partial['artist_name'].tolist()

ax.set_xlabel('playtime (in ms)')
xticks = np.arange((min(x)//3600000)//10*10, (max(x)//3600000) + 1, 10)
ax.set_xticks(ticks=[t*3600000 for t in xticks], labels=xticks) # scuffed labels
ax.set_ylabel('playcount')
yticks = np.arange((min(y))//100*100, (max(y)) + 1, 100)
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
    text = "{} - {}\nplaytime: {}\nplaycount: {}".format(track_names[n], artist_names[n], convert_ms(x[n]), y[n])
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