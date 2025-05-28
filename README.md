# musicstats_spotify

0. download extended streaming history from spotify 
1. put data in data folder
2. run sortbytrack.py
3. run sortbyartist.py
4. run other files 

:3


# programs 
sortbytrack.py: makes tracks.csv based off of raw data; includes playcount, playtime
sortbyartist.py: makes artists.csv based off of tracks.csv; includes playcount, playtime, and unique tracks

graphartists_playtime.py: graph top n artists by playtime (reads from artists.csv)
graphartists_playcount.py: graph top n artists by playcount (reads from artists.csv)
graphartists_uniquetracks.py: graph top n artists by uniquetracks (reads from artists.csv)
graphartists_compare.py: graphs top n tracks by playtime, comparing playcount to unique tracks (reads from tracks.csv)

graphtracks_playtime.py: graph top n tracks by playtime (reads from tracks.csv)
graphtracks_playcount.py: graphs top n tracks by playcount (reads from tracks.csv)
graphtracks_compare.py: graphs top n tracks by playtime, comparing playcount to playtime (reads from tracks.csv)

makenicelists.py: self explanatory. (reads from tracks.csv, artists.csv)
totaltimeplayed.py: self explanatory (reads from tracks.csv)

graphALLtracks.py: scatterfm style graphing. hella slow :>