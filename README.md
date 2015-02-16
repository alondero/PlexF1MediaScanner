Simple PlexF1MediaScanner
==================

Forked from PlexF1MediaScanner.

A more simple version of the PlexF1MediaScanner that can handle any season (not just 2014). Read that readme for more details about why the project came about.

Currently this relies upon a file structure of <YEAR>/<YEAR> - s<RACE_NUMBER>e<QUALIFYING OR RACE?1:2> - <COUNTRY>.

For example 1998/1998 - s01e01 - Australia, which represents the Qualifying session for the 1998 Australian GP. 

WIP - Metadata Agent to go with this, grabbing a better title and description from Wikipedia? 
 
Install and use:

clone repository
modify Formula1.py to correct the location of your plex directory
copy the attached file to <PLEX DIRECTORY>/Library/Application Support/Plex Media Server/Scanners/Series/
restart plexmediaserver
Add a new Television library and add the folder containing F1 broadcasts
Select Advanced and Scanner: Formula1
 
Bugs:
You have to re-add the library when you get new files, because it adds a new show with the same name for the new files, why?
The way it increments the episode numbers might be lost from scan to scan? Have not verified due to the bug above.
 
If you have suggestions how to fix the bugs, please let me know.
