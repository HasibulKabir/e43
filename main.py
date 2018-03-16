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
import eyed3
import random
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import soundcloud
import string

reload(sys)
sys.setdefaultencoding("utf-8")

client = soundcloud.Client(client_id='LBCcHmRB8XSStWL6wKH2HPACspQlXg2P')

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = ""
f = open("random.txt", "w+")
f.write(str(random.randint(20,30)))
f.close()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(chat_type)
    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print(flavor, summary, chat_type)
    f = open("random.txt", "r")
    rnumber = int(f.read())
    f.close()
    if content_type == 'audio':
        audiofile = msg['audio']
        fileid = msg['audio']['file_id']
        flavor = telepot.flavor(msg)
        summary = telepot.glance(msg, flavor=flavor)
        print(flavor, summary)
        print(fileid)
        print(bot.getFile(file_id=fileid))
        filename = bot.getFile(file_id=fileid)['file_path']
        os.system("wget https://api.telegram.org/file/bot" + TOKEN + "/" + filename + " -O " + filename)
        if ".mp3" in filename:
            audio = MP3(filename)
            length = audio.info.length * 0.33
            l2 = (audio.info.length * 0.33) + 60
        if ".m4a" in filename:
            audio = MP4(filename)
            length = audio.info.length * 0.33
            l2 = (audio.info.length * 0.33) + 60
        if audio.info.length > l2:
            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
        else:
            os.system("ffmpeg -ss 0 -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
        sendVoice(chat_id, "output.ogg")
    if content_type == "text":
        if msg['text'].startswith("/conv http://") or msg['text'].startswith("/conv https://") and not chat_type == "channel":
            try:
                bot.sendMessage(chat_id, "Please wait...I'm converting the URL to an MP3 file")
                input_text = msg['text'].split("/conv ")[1]
                if "soundcloud" in input_text:
                    try:
                        track = client.get('/resolve', url=input_text)
                        thist = track
                        filename = thist.title.replace(" ", "_").replace("!", "_").replace("&", "_").replace("?", "_") + ".mp3"
                        stream_url = client.get(thist.stream_url, allow_redirects=False)
                        artist = None
                        title = None
                        try:
                            printable = set(string.printable)
                            artist = filter(lambda x: x in printable, thist.title.split(" - ")[0])
                            printable = set(string.printable)
                            title = filter(lambda x: x in printable, thist.title.split(" - ")[1])
                            os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                            os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                            os.system("lame -V0 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                        except:
                            printable = set(string.printable)
                            artist = filter(lambda x: x in printable, thist.user['username'])
                            printable = set(string.printable)
                            title = filter(lambda x: x in printable, thist.title)
                            os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                            os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                            os.system("lame -V0 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                        bot.sendMessage(chat_id, "Sending the file...")
                        print(filename)
                        sendAudio(chat_id,filename,artist,title)
                        audio = MP3(filename)
                        length = audio.info.length * 0.33
                        l2 = length + 60
                        if audio.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        sendVoice(chat_id, "output.ogg")
                        bot.sendMessage(chat_id,"Here you go!")
                    except:
                        bot.sendMessage(chat_id, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
                else:
                    if "youtu" in input_text:
                        cmd = 'youtube-dl --add-metadata -x --prefer-ffmpeg --extract-audio -v --audio-format mp3 \
                            --output audio.%%(ext)s %summary'%(input_text)
                        subprocess.check_call(cmd.split(), shell=False)
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
                        subprocess.Popen(["sacad", artist, title, "800", "audio.jpg"], shell=False).wait()
                        subprocess.Popen(["lame", "-V", "0", "-b", "320", "--ti", "audio.jpg", "--tt", title, "--ta", artist , "audio.mp3"], shell=False).wait()
                        bot.sendMessage(chat_id,"Sending the file...")
                        filename = artist.replace(" ", "_") + "-" + title.replace(" ", "_") + ".mp3"
                        try:
                            os.rename("audio.mp3.mp3", filename)
                        except:
                            try:
                                os.rename("audio.mp3", filename)
                            except:
                                try:
                                    filename = "audio.mp3.mp3"
                                except:
                                    try:
                                        filename = "audio.mp3"
                                    except:
                                        bot.sendMessage(chat_id, "Uh-oh, something miserably bad happened. Contact @Sommerlichter, he might fix this.")
                        sendAudio(chat_id, filename, artist, title)
                        audio = eyed3.load("audio.mp3")
                        tt = audio.tag.title
                        artist = audio.tag.artist
                        ad = MP3("audio.mp3")
                        length = ad.info.length * 0.33
                        l2 = length + 60
                        if ad.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"audio.mp3\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"audio.mp3\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        sendVoice(chat_id, "output.ogg")
                        bot.sendMessage(chat_id,"Here you go!")
                    else:
                        url = msg['text'].split("/conv ")[1]
                        filename = subprocess.check_output(["node", "--no-warnings", "download-url.js", url]).split('\n')[0]
                        os.system("ffmpeg -y -i \"" + filename + "\" -codec:a libmp3lame -qscale:a 0 -map_metadata 0:g output.mp3")
                        bot.sendMessage(chat_id, "Sending the file...")
                        audio = eyed3.load(filename)
                        tt = audio.tag.title
                        artist = audio.tag.artist
                        filename = artist.replace(" ", "_") + "-" + tt.replace(" ", "_") + ".mp3"
                        os.rename("output.mp3", filename)
                        sendAudio(chat_id, filename, artist, tt)
                        audio = MP3(filename)
                        length = audio.info.length * 0.33
                        l2 = length + 60
                        if audio.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        sendVoice(chat_id, "output.ogg")
                        bot.sendMessage(chat_id,"Here you go!")
            except:
                bot.sendMessage(chat_id, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
        else:
            if "😂" in msg['text']:
                count = len(msg['text'].split("😂")) - 1
                f = open("counters/joy.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/joy.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "😂 level is now: " + str(sum))
            if "bro" in msg['text']:
                count = len(msg['text'].split("bro")) - 1
                f = open("counters/bro.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/bro.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "bro level is now: " + str(sum))
            if "Hi" in msg['text']:
                count = len(msg['text'].split("Hi")) - 1
                f = open("counters/hi.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/hi.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "Hi level is now: " + str(sum))
            if "lol" in msg['text']:
                count = len(msg['text'].split("lol")) - 1
                f = open("counters/lol.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/lol.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "lol level is now: " + str(sum))
            if "pp" in msg['text']:
                count = len(msg['text'].split("pp")) - 1
                f = open("counters/pp.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/pp.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "pp level is now: " + str(sum))
            if msg['text'].startswith("/ping"):
                bot.sendMessage(chat_id, "Pong!")
            if msg['text'].startswith("/start") and chat_type == "private":
                bot.sendMessage(chat_id,"Hello, please send me the name of the song or an URL from Soundcloud, YouTube and many more I have to convert :)")
            if chat_type == "private" and msg["text"].startswith("http"):
                try:
                    bot.sendMessage(chat_id, "Please wait...I'm converting the URL to an MP3 file")
                    input_text = msg['text']
                    if "soundcloud" in input_text:
                        try:
                            track = client.get('/resolve', url=input_text)
                            thist = track
                            filename = thist.title.replace(" ", "_").replace("!", "_").replace("&", "_").replace("?", "_") + ".mp3"
                            stream_url = client.get(thist.stream_url, allow_redirects=False)
                            artist = None
                            title = None
                            try:
                                printable = set(string.printable)
                                artist = filter(lambda x: x in printable, thist.title.split(" - ")[0])
                                printable = set(string.printable)
                                title = filter(lambda x: x in printable, thist.title.split(" - ")[1])
                                os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                                os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                                os.system("lame -V0 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                            except:
                                printable = set(string.printable)
                                artist = filter(lambda x: x in printable, thist.user['username'])
                                printable = set(string.printable)
                                title = filter(lambda x: x in printable, thist.title)
                                os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                                os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                                os.system("lame -V0 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                            bot.sendMessage(chat_id, "Sending the file...")
                            print(filename)
                            sendAudio(chat_id,filename,artist,title)
                            audio = MP3(filename)
                            length = audio.info.length * 0.33
                            l2 = length + 60
                            if audio.info.length > l2:
                                os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                            else:
                                os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                            sendVoice(chat_id, "output.ogg")
                            bot.sendMessage(chat_id,"Here you go!")
                        except:
                            bot.sendMessage(chat_id, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
                    else:
                        if "youtu" in input_text:
                            cmd = 'youtube-dl --add-metadata -x --prefer-ffmpeg --extract-audio -v --audio-format mp3 \
                                --output audio.%%(ext)s %summary'%(input_text)
                            subprocess.check_call(cmd.split(), shell=False)
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
                            subprocess.Popen(["sacad", artist, title, "800", "audio.jpg"], shell=False).wait()
                            subprocess.Popen(["lame", "-V", "0", "-b", "320", "--ti", "audio.jpg", "--tt", title, "--ta", artist , "audio.mp3"], shell=False).wait()
                            bot.sendMessage(chat_id,"Sending the file...")
                            filename = artist.replace(" ", "_") + "-" + title.replace(" ", "_") + ".mp3"
                            try:
                                os.rename("audio.mp3.mp3", filename)
                            except:
                                try:
                                    os.rename("audio.mp3", filename)
                                except:
                                    try:
                                        filename = "audio.mp3.mp3"
                                    except:
                                        try:
                                            filename = "audio.mp3"
                                        except:
                                            bot.sendMessage(chat_id, "Uh-oh, something miserably bad happened. Contact @Sommerlichter, he might fix this.")
                            sendAudio(chat_id, filename, artist, title)
                            audio = eyed3.load("audio.mp3")
                            tt = audio.tag.title
                            artist = audio.tag.artist
                            ad = MP3("audio.mp3")
                            length = ad.info.length * 0.33
                            l2 = length + 60
                            if ad.info.length > l2:
                                os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"audio.mp3\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                            else:
                                os.system("ffmpeg -ss 0 -t 60 -y -i \"audio.mp3\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                            sendVoice(chat_id, "output.ogg")
                            bot.sendMessage(chat_id,"Here you go!\nConsider a small donation at https://koyu.space/support if you like this bot :)",disable_web_page_preview=True)
                        else:
                            url = msg['text']
                            filename = subprocess.check_output(["node", "--no-warnings", "download-url.js", url]).split('\n')[0]
                            os.system("ffmpeg -y -i \"" + filename + "\" -codec:a libmp3lame -qscale:a 0 -map_metadata 0:g output.mp3")
                            bot.sendMessage(chat_id, "Sending the file...")
                            audio = eyed3.load(filename)
                            tt = audio.tag.title
                            artist = audio.tag.artist
                            filename = artist.replace(" ", "_") + "-" + tt.replace(" ", "_") + ".mp3"
                            os.rename("output.mp3", filename)
                            sendAudio(chat_id, filename, artist, tt)
                            audio = MP3(filename)
                            length = audio.info.length * 0.33
                            l2 = length + 60
                            if audio.info.length > l2:
                                os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                            else:
                                os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                            sendVoice(chat_id, "output.ogg")
                            bot.sendMessage(chat_id,"Here you go!\nConsider a small donation at https://koyu.space/support if you like this bot :)",disable_web_page_preview=True)
                except:
                    bot.sendMessage(chat_id, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
            if chat_type == "private" and not msg['text'].startswith("/start") and not msg['text'].startswith("/ping") and not msg['text'].startswith("http") and not msg['text'].startswith("/conv"):
                try:
                    bot.sendMessage(chat_id, "Please wait...I'm converting the song to an MP3 file")
                    input_text = msg['text']
                    url = subprocess.check_output(["node", "--no-warnings", "download.js", input_text]).split('\n')[0]
                    filename = subprocess.check_output(["node", "--no-warnings", "download-url.js", url]).split('\n')[0]
                    fname = filename
                    os.system("ffmpeg -y -i \"" + filename + "\" -codec:a libmp3lame -qscale:a 0 -map_metadata 0:g output.mp3")
                    bot.sendMessage(chat_id, "Sending the file...")
                    audio = eyed3.load(filename)
                    tt = audio.tag.title
                    artist = audio.tag.artist
                    try:
                        filename = artist.replace(" ", "_") + "-" + tt.replace(" ", "_") + ".mp3"
                        os.rename("output.mp3", filename)
                        sendAudio(chat_id, filename, artist, tt)
                        audio = MP3(filename)
                        length = audio.info.length * 0.33
                        l2 = length + 60
                        if audio.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    except:
                        sendAudio(chat_id, fname, artist, tt)
                        audio = MP3(fname)
                        length = audio.info.length * 0.33
                        l2 = length + 60
                        if audio.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + fname + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + fname + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    sendVoice(chat_id, "output.ogg")
                    bot.sendMessage(chat_id,"Here you go!\nConsider a small donation at https://koyu.space/support if you like this bot :)",disable_web_page_preview=True)
                except:
                    bot.sendMessage(chat_id, "I cannot find the song you're looking for. Go find yourself a link and enter it here, so I know where to start from.")

def sendAudio(chat_id,file_name,performer,title):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'performer' : performer, 'title' : title}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendAudio2(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendVoice(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendVoice"%(TOKEN)
    files = {'voice': open(file_name, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening ...')

while 1:
    time.sleep(10)
