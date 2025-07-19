import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import tz
import os # for file name sutff


timezone_offset = -8 # in hours, from utc (ie what do u add to utc to get the timezone)
dot_size = 0.04
labels = True
colors = True

plt.rcParams['font.family'] = ['Heiti TC'] # choose font that includes non latin characters


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

# print(jsons)


cleaneddata = [] # list of all plays of songs

for jsonpath in jsons:
    if jsonpath.split(".")[-1] != "json":
        continue
    data = pd.read_json(jsonpath)
    cleaneddata.append(data[["master_metadata_album_artist_name", 
                             "master_metadata_track_name", 
                             "ts"]])
totaldata = pd.concat(cleaneddata) 


x = []
y = []
c = []
l = []

for n, row in totaldata.iterrows():
    ts = row['ts']
    track = row['master_metadata_track_name']
    artist = row['master_metadata_album_artist_name']
    
    if not track is None and not artist is None:
        utc_time = datetime.fromisoformat(ts[:-1])
        unix_time = int(utc_time.strftime('%s')) # in utc
        unix_naive_cur_timezone = unix_time + 3600*timezone_offset # in current timezone
        x.append((unix_time - 3600*timezone_offset)//86400)
        y.append(86400-(unix_time - 3600*timezone_offset)%86400)

        timezone_correct = datetime.fromtimestamp(unix_naive_cur_timezone)
        l.append(artist + " - " + track + "\n" + str(timezone_correct)) # fix later convert to local timezone
        
        if colors:
            h = hash(artist) # really stupid color generator thing
            c.append((h%1000 / 1000, (h//1000)%1000 / 1000, (h//1000000)%1000 / 1000))

fig, ax = plt.subplots(figsize=(15, 7))

if colors: 
    sc = ax.scatter(x, y, s=dot_size, c=c)
else:
    sc = ax.scatter(x, y, s=dot_size)

if labels: 

    annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

def update_annot(ind):
    n = ind["ind"][0]

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = l[n]
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

# old testing stuff below ignroe idk 

# ts = "2023-11-16T23:56:30Z"

# utc_time = datetime.fromisoformat(ts[:-1])
# print("utc: " + str(utc_time))

# unix_time = utc_time.strftime('%s')

# y = (utc_time - 3600*8)%86400
# x = (utc_time - 3600*8)//86400