from __future__ import print_function
from moviepy.editor import *
import urllib
import urllib2
from bs4 import BeautifulSoup
from pytube import YouTube
import sys

videos = list()

songfile = open("song_list", 'r')

for line in songfile:
    videos.append(line)

for videotext in videos:
    videoarray = videotext.split(',')
    print(videoarray)
    artist = videoarray[0]
    song = videoarray[1].rstrip('\n')
    songtext = urllib.quote(artist + "-" + song)
    url = "https://www.youtube.com/results?search_query=" + songtext
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    souplist = soup.findAll(attrs={'class':'yt-uix-tile-link'})
    videolink = "https://www.youtube.com" + souplist[0]['href']
    print(videolink)
    yt = YouTube(videolink)
    filename = artist + "-" + song
    yt.set_filename(filename)
    vidinfo = yt.filter('mp4')[-1]
    print(yt.filter('mp4'))
    try:
        video = yt.get('mp4',vidinfo.resolution)
        video.download('/tmp')
    except OSError:
        print("File Already Exists, continuing.")
    videoClip = VideoFileClip("/tmp/"+filename+".mp4")
    w,h = videoClip.size

    text = TextClip(filename, font='Times-Roman',
                    color='white', fontsize=20)
    text_color = text.on_color(size=(videoClip.w + text.w,text.h+10),
                               color=(0,0,0), pos=(6,'center'),
                               col_opacity=0.6)
    text_anim = text_color.set_position(
        lambda t: (max(w/30,int(w-0.5*w*t)),max(5*h/6, int(100*t))) )

    final = CompositeVideoClip([videoClip,text_anim])
    final.set_duration(videoClip.duration).write_videofile('/tmp/final_'+filename+".mp4", codec='libx264')





