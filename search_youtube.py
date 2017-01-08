from __future__ import print_function
import urllib
import urllib2
from bs4 import BeautifulSoup
from pytube import YouTube

videos = list()

songfile = open("song_list", 'r')

for line in songfile:
    videos.append(line)

for videotext in videos:
    videoarray = videotext.split(',')
    print(videoarray)
    artist = videoarray[0].replace(" ", "")
    song = videoarray[1].rstrip('\n')
    songtext = urllib.quote(song)
    url = "https://www.youtube.com/results?search_query=" + artist + "-" + songtext
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    souplist = soup.findAll(attrs={'class':'yt-uix-tile-link'})
    videolink = "https://www.youtube.com" + souplist[0]['href']
    print(videolink)
    yt = YouTube(videolink)
    yt.set_filename(artist + "-" + song)
    video = yt.get('mp4')
    video.download('/tmp')



