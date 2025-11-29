import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import tz
from colorsys import hsv_to_rgb
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

# Filter out None values upfront
totaldata = totaldata.dropna(subset=['master_metadata_track_name', 'master_metadata_album_artist_name'])

# Vectorized conversion to unix time
totaldata['unix_time'] = pd.to_datetime(totaldata['ts']).astype(np.int64) // 10**9

# Vectorized x, y calculations
x = (totaldata['unix_time'] + 3600*timezone_offset) // 86400
y = 86400 - (totaldata['unix_time'] + 3600*timezone_offset) % 86400

# Create labels with timezone correction
unix_naive_cur_timezone = totaldata['unix_time'] + 3600*timezone_offset
timezone_correct = pd.to_datetime(unix_naive_cur_timezone, unit='s')
l = (totaldata['master_metadata_album_artist_name'] + " - " + 
     totaldata['master_metadata_track_name'] + "\n" + 
     timezone_correct.dt.strftime("%m/%d/%Y | %I:%M %p")).tolist()

# Vectorized color generation
if colors:
    def get_color(artist):
        h = hash(artist)
        hue = (h % 360) / 360.0  # 0-1 hue range for better color spread
        saturation = 0.6 + ((h // 360) % 40) / 100.0  # vary saturation slightly
        value = 0.8 + ((h // 36000) % 20) / 100.0  # vary brightness slightly
        return hsv_to_rgb(hue, saturation, value)
    
    c = [get_color(artist) for artist in totaldata['master_metadata_album_artist_name']]
else:
    c = []

# Convert to numpy arrays for faster access
x_array = x.values
y_array = y.values
l_array = np.array(l)


fig, ax = plt.subplots(figsize=(15, 7))

if colors: 
    sc = ax.scatter(x, y, s=dot_size, c=c)
else:
    sc = ax.scatter(x, y, s=dot_size)

# Cache offsets for faster hover
offsets = sc.get_offsets()

# y axis ticks: time of day (in 4 hr)
hours_in_seconds = [i * 4 * 3600 for i in range(6)] 
hour_labels = [datetime.fromtimestamp(h - 3600*timezone_offset).strftime("%I:%M %p") for h in hours_in_seconds]
ax.set_yticks([(86400 - h) for h in hours_in_seconds])
ax.set_yticklabels(hour_labels)


# x axis ticks: date (in 6 month increments)
min_day = min(x)
max_day = max(x)
    
min_date = datetime.fromtimestamp((min_day * 86400) - 3600*timezone_offset)
max_date = datetime.fromtimestamp((max_day * 86400) - 3600*timezone_offset)
    
date_ticks = []
date_labels = []
current = min_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
if current.month < 7:
    current = current.replace(month=1)
else:
    current = current.replace(month=7)
    
while current <= max_date:
    day_num = int((current.timestamp() + 3600*timezone_offset) // 86400)
    date_ticks.append(day_num)
    date_labels.append(current.strftime("%b %Y"))
        
    if current.month == 1:
        current = current.replace(month=7)
    else:
        current = current.replace(year=current.year + 1, month=1)
    
ax.set_xticks(date_ticks)
ax.set_xticklabels(date_labels)

if labels: 

    annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

def update_annot(ind):
    n = ind["ind"][0]
    pos = offsets[n]
    annot.xy = pos
    annot.set_text(l_array[n])
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont and len(ind["ind"]) > 0:
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