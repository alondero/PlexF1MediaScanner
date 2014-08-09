PlexF1MediaScanner
==================

The way that Formula1 boadcasts is organized doesn't fit very well with ether Movies or TV Series. Adding them as home movies is one unsatisfactory option, but instead I tried to make a Formula1 Media Scanner.
 
It is working for my purpose, and I take no responsibility should it cause you any harm, but you are free to reuse and modify it.
 
How it works:
 
I typically have all my Formula1 media in one folder, and one broadcast can be named i.e. formula1.2014.spain.grand.prix.qualifying.uncut.720p.hdtv.x264.mkv. The Formula1 Media Scanner picks up the various parts of the file name using this regular expression:
'(?P<show>.*?)[\._ ](?P<season>[0-9]{4})[\._ ](?P<location>.*?)[\.](?P<ep>.*?)\.(720p|HDTV|x254|1080p)'
 
In the above example it will find the following match:
MATCH 1
show [1-9] `formula1`
season [10-14] `2014`
location [15-20] `spain`
ep [21-48] `grand.prix.qualifying.uncut`
5. [49-53] `720p`
 
 
The challenge here is to map this into a TV Series format. Basically a Formula1 episode is really a full weekend, containing many broadcasts, from buildup, FP1-3, Qualifying, race and others. However, one episode may only contain one media (disregarding stacking, as that is really sub optimal here).
What I did instead was to assume that this library will only contain Formula1, and I named the show like Formula1 yyyy. So for the example above, the show would resolv to Formula1 2014.
A series is then mapped to a location, but since series unfortunately only supports integer, I made a look up table to resolve location to Season number (This will have to be updated for years to come, only 2014 added).
Under a given season (location) I add all the media pertaining to this location (weekend) as episodes.
If it encounters a locations it doesn't recognize, it will still add the episode, but under season 99 (unknown)
 
Thinking out loud
Ideally I could add a show as Formula1, add seasons by year, add Episodes as location. Opening one Episode allows you to play any file from that weekend, but I don't see how that can be done.
This scanner should work well for others (motor)sports that are organized in a similar way, you have to update locations though.
The locations could be added dynamically, but I have added them manually so I get the "Seasons" in the correct order of the calender.
 
 
Install and use:
 
copy the attached file to /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners/Series/
restart plexmediaserver
Add a new library called Formula1 and add the folder containing F1 broadcasts
Select Advanced and Scanner: Formula1
 
Bugs:
You have to re-add the library when you get new files, because it adds a new show with the same name for the new files, why?
The way it increments the episode numbers might be lost from scan to scan? Have not verified due to the bug above.
 
If you have suggestions how to fix the bugs, please let me know.
