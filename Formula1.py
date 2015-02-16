#!/usr/bin/env python

import sys
import os
import logging

#Modify these paths to be the location of Plex
sys.path.append("...../plex/Library/Application Support/Plex Media Server/Scanners/Series")
sys.path.append("...../plex/Library/Application Support/Plex Media Server/Plug-ins/Scanners.bundle/Contents/Resources/Common/")

import re
import Media
import VideoFiles
import Stack
import Utils

sessionmap = {
	1: "Qualifying",
	2: "Race"
}

episode_regexp = '(?P<year>.*?)\s-\ss(?P<race>[0-9]{2})e(?P<session>0[1-2])\s-\s(?P<episode>[^\.]*)'

def Scan(path, files, mediaList, subdirs, language=None, root=None):
	VideoFiles.Scan(path, files, mediaList, subdirs, root)
	
	for i in files:
		logging.debug("file:"+i)
        file = os.path.basename(i)
        logging.debug("basename:"+file)
        match = re.search(episode_regexp, file, re.IGNORECASE)
        if match:
			year = match.group('year')
			race = int(match.group('race'))
			sessionnumber = int(match.group('session'))
			session = sessionmap[sessionnumber]
			episode = match.group('episode')
			
			logging.debug("Found F1 episode - Year: %d, Race: %d, Session: %s, Episode: %s", year, race, session, episode)
			
			racetitle = year + " " + str(episode) + " Grand Prix"
			description = session + " - " + racetitle
			
			tv_show = Media.Episode(year, race, sessionnumber, description, year)	
			tv_show.parts.append(i)
			mediaList.append(tv_show)
			logging.debug("tv_show created")
	Stack.Scan(path, files, mediaList, subdirs)

