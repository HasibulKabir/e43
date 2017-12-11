#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import time
import telepot

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
        bot.sendMessage(chat_id, "Please wait...I'm converting the link to an MP3 file")
        file = os.popen("node --no-warnings download.js " + input_text).read()
        sendAudio(chat_id, file)
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
