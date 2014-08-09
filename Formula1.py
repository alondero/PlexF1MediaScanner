#!/usr/bin/env python

#     Copyright (C) 2013  Casey Duquette
# 
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

"""
Custom scanner plugin for Plex Media Server for Formula1 Brodcast.
"""

import re, os, os.path
import sys
import logging

# I needed some plex libraries, you may need to adjust your plex install location accordingly
sys.path.append("/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners/Series")
sys.path.append("/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/Scanners.bundle/Contents/Resources/Common/")
import Media, VideoFiles, Stack, Utils
from mp4file import mp4file, atomsearch

__author__ = "Kenneth Ellefsen"
__copyright__ = "Copyright 2014"
__credits__ = ["Kenneth Ellefsen"]

__license__ = "GPLv2"
__version__ = "1.0"
__maintainer__ = "Kenneth Ellefsen"
__email__ = ""


locations = { 2014 : 
                {
                'australia' : 1,
                 'malaysia' : 2,
                 'bahrain' : 3,
                 'china' : 4,
                 'chinese' : 4,
                 'spain' : 5,
                 'spanish' : 5,
                 'monaco' : 6,
                 'canadian' : 7,
                 'canada' : 7,
                 'austrian' : 8,
                 'austria' : 8,
                 'british' : 9,
                 'great britain' : 9,
                 'german' : 10,
                 'germany' : 10,
                 'hungarian' : 11,
                 'hungary' : 11,
                 'belgian' : 12,
                 'belgium' : 12,
                 'italian' : 13,
                 'italyn' : 13,
                 'singapore' : 14,
                 'japanese' : 15,
                 'japan' : 15,
                 'russian' : 16,
                 'russia' : 16,
                 'united states' : 17,
                 'us' : 17,
                 'brazilian' : 18,
                 'brazil' : 18,
                 'abu dhabi' : 19,
                 'unknown' : 99,
                 } ,
             }

locationsep = { 2014 :
                {
                1 : 0,
                2 : 0,
                3 : 0,
                4 : 0,
                5 : 0,
                6 : 0,
                7 : 0,
                8 : 0,
                9 : 0,
                10 : 0,
                11 : 0,
                12 : 0,
                13 : 0,
                14 : 0,
                15 : 0,
                16 : 0,
                17 : 0,
                18 : 0,
                19 : 0,
                99 : 0,
                },
              }


#episode_regexp = '(?P<show>formula1|f1?)[\._ ](?P<season>[0-9]{4})[\._ ](?P<location>.*?)[\.](?P<ep>.*?)\.(720p|HDTV|x254|1080p)'
episode_regexp = '(?P<show>.*?)[\._ ](?P<season>[0-9]{4})[\._ ](?P<location>.*?)[\.](?P<ep>.*?)\.(720p|HDTV|x254|1080p)'


# Look for episodes.
def Scan(path, files, mediaList, subdirs, language=None, root=None):
    # Scan for video files.
    VideoFiles.Scan(path, files, mediaList, subdirs, root)
  
    logging.basicConfig(filename='/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Formula1.log',level=logging.DEBUG)
    #comment the line below to enable debugging
    #logging.disable(logging.DEBUG)

    logging.debug("path:"+path)

    # Run the select regexp for all media files.
    for i in files:
        logging.debug("file:"+i)
        file = os.path.basename(i)
        logging.debug("basename:"+file)
        match = re.search(episode_regexp, file, re.IGNORECASE)
        if match:
            # Extract data.
            location = match.group('location').lower().replace("."," ")         # Location typically Spain/Spanish/Italy ...
            origlocation = location
            show = 'formula1' if match.group('show').lower() == 'f1' else match.group('show').strip()
            year = match.group('season').strip()
            yearint = int(year)
            logging.debug("year:%s",year)
            show = show + " " + year # Make a composite show name like Formula1 + yyyy
            logging.debug("looking for location:%s in locations[%d]",location,yearint)
            if location not in locations[yearint].viewkeys():
                location = "unknown"
                logging.debug("location not found, mapping %s to unknown",location)
#                continue

            locationidx = locations[yearint][location] #location index is mapped to season
            locationsep[yearint][locationidx] += 1 # count up ep number for each matching file for a given location

            # episode is just a meaningless index to get the different FP1-3, Qualifying, Race and other files to
            # be listed under a location i.e. Spain, which again is mapped to season number - as season can not contain a string
            episode = locationsep[yearint][locationidx] 

            # description will be the displayed filename when you browse to a location (season number)

            logging.debug("show:"+show)
            logging.debug("location:"+location)
            logging.debug("episode%d:",episode)
            description = "";

            if location == "unknown": # reset the location back to get full description
                location = origlocation
                logging.debug("resetting location to:%s",origlocation)

            description = location + " " + match.group('ep').replace("."," ") # i.e. # spain grand prix free practice 3
            logging.debug("description:"+description)

            tv_show = Media.Episode(
                show,               # show (inc year(season))
                locationidx,        # locationidx as season (string not supported) 
                episode,            # episode, indexed the files for a given show/location
                description,        # includes location string and ep name i.e. Spain Grand Prix Qualifying
                year)               # the actual year detected, same as used in part of the show name

            logging.debug("tv_show created")
            tv_show.parts.append(i)
            logging.debug("part added to tv_shows")
            mediaList.append(tv_show)
            logging.debug("added tv_show to mediaList")
        else:
            logging.debug("no match")

  
    # Stack the results.
    Stack.Scan(path, files, mediaList, subdirs)

def find_data(atom, name):
  child = atomsearch.find_path(atom, name)
  data_atom = child.find('data')
  if data_atom and 'data' in data_atom.attrs:
    return data_atom.attrs['data']

import sys
    
if __name__ == '__main__':
  print "Hello, world!"
  path = sys.argv[1]
  files = [os.path.join(path, file) for file in os.listdir(path)]
  media = []
  Scan(path[1:], files, media, [])
  print "Media:", media


