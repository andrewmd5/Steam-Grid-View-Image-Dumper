'''
Created on Sep 24, 2013

@author: Andrew/Codeusa
http://blog.codeusa.net
'''
import sys
import urllib.request
import re
import os.path
import time


def get_app_ids(appstring):
    index = '"appid":'
    substring = 0
    while True:
        substring = appstring.find(index, substring)
        if substring == -1: 
            return
        pattern = re.compile('(\"appid":)([0-9]+)')
        match = pattern.match(appstring, substring)
        resolve = int(match.group(2))
        substring += len(match.group())
        yield resolve


username = input("Enter your steam profile username: ")

profileURL = "http://steamcommunity.com/id/" + username + "/games?tab=all"
stream = urllib.request.urlopen(profileURL)
if stream is None:
    print("Stream produced nothing or did not load, failing obviously")
    sys.exit()

try:
    os.mkdir("griddump")
except OSError:
    pass

app_ids = []
for line in stream:
    line = str(line, encoding='utf8')
    for appid in get_app_ids(line):
        app_ids.append(appid)

for appid in app_ids:
    path = "griddump/" + str(appid) + ".png"
    '''
    #_by using header.png you can grab other versions of the grid.
    #For example Modern Warfare produced a multiplayer grid icon.
    '''
    profileURL = "http://cdn.steampowered.com/v/gfx/apps/" + str(appid) + "/header.jpg"
    if os.path.exists(path):
        print("Already did this one, moving on. AppID: " + str(appid))
        continue

    try:
        stream = urllib.request.urlopen(profileURL)
    except urllib.error.HTTPError:
        print("Can't stream URL " + str(appid))
        continue

    f = open(path, 'wb')
    f.write(stream.read())
    print("Downloading Grid for AppID: " + str(appid))
    time.sleep(2)
