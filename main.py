#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import time
import telepot
import requests
import os
import re
import requests
import subprocess
import urlparse
import time
import re

TOKEN = ""

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    input_text = msg['text']
    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print(flavor, summary)
    if input_text.startswith("/start"):
        bot.sendMessage(chat_id,"Hello, please send me the name of the song or a link from YouTube, Spotify, Deezer and many more :)")
    else:
        bot.sendMessage(chat_id, "Please wait...I'm converting the song to an MP3 file")
        metadata = os.popen("node --no-warnings download.js " + input_text).read()
        cmd = 'youtube-dl --add-metadata -x --prefer-ffmpeg --extract-audio --write-thumbnail --embed-thumbnail -v --audio-format mp3 \
            --output "audio.%%(ext)s" %summary'%(metadata)
        os.system(cmd)
        url_data = urlparse.urlparse(metadata)
        query = urlparse.parse_qs(url_data.query)
        #video = query["v"][0]
        #os.system("wget -O audio.jpg http://i4.ytimg.com/vi/" + video + "/default.jpg")
        cmd = ["youtube-dl", "--get-title", "--skip-download", metadata]
        output = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0]
        output = output.split("\n")[0]
        time.sleep(3)
        tag = eyed3.load("audio.mp3")
	try:
          title = tag.tag.title.split(" - ")[1]
          artist = tag.tag.title.split(" - ")[0]
	  title = title.replace(artist + " - ","")
	  try:
	    if not "Remix" in title and not "Mix" in title:
	      title = title.split(" (")[0]
	  except:
	    pass
	  try:
	    title = title.split(" [")[0]
	  except:
	    pass
	except:
	  title = tag.tag.title
	  artist = tag.tag.artist
	#bot.sendMessage(chat_id,artist+" - "+title)
	os.system("sacad '" + artist + "' '" + title + "' 800 audio.jpg")
        os.system("lame -V 0 -b 128 --ti audio.jpg --tt \"" + title + "\" --ta \"" + artist + "\" audio.mp3")
        bot.sendMessage(chat_id,"Sending the file...")
	filename = artist.replace(" ", "_") + "-" + title.replace(" ", "_") + ".mp3"
	os.rename("audio.mp3.mp3", filename)
        sendAudio(chat_id,filename)
        bot.sendMessage(chat_id,"Here you go!\nConsider a small donation at https://koyu.space/support if you like this bot :)")

def sendAudio(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening ...')

while 1:
    time.sleep(10)
