#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import time
import telepot
import requests
import os
import os.path
import re
import requests
import subprocess
import time
import re
import eyed3
import random
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import soundcloud
import string
import pylast
import json
import urllib
from HTMLParser import HTMLParser
from youtube_title_parse import get_artist_title

reload(sys)
sys.setdefaultencoding("utf-8")

# Initializing APIs
client = soundcloud.Client(client_id='LBCcHmRB8XSStWL6wKH2HPACspQlXg2P')
API_KEY = "9d3ee2a574eb3bb2a6f0a4e108e46ceb"
API_SECRET = "f982de3bd2d8e7ffe5c117b568b1fc3e"
lastfm = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
html = HTMLParser()
thumb = "thumb.jpg"

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = ""
if 'BOTMASTER' in os.environ:
    BOTMASTER = os.environ.get('BOTMASTER')
else:
    BOTMASTER = 'Sommerlichter'
f = open("random.txt", "w+")
f.write(str(random.randint(10,30)))
f.close()

def handle(msg):
    done = False
    bottag = bot.getMe()["username"]
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(chat_type)
    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print(flavor, summary, chat_type)
    f = open("random.txt", "r")
    rnumber = int(f.read())
    f.close()
    if chat_type == "private":
        try:
            f = open("chatids.txt", "r")
            s = f.read()
            f.close()
            if not str(chat_id) in s:
                f = open("chatids.txt", "a+")
                f.write(str(chat_id) + "\n")
                f.close()
        except:
            pass
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
            audio = MP3(ucode(filename))
            length = audio.info.length * 0.33
            l2 = (audio.info.length * 0.33) + 60
        if ".m4a" in filename:
            audio = MP4(filename)
            length = audio.info.length * 0.33
            l2 = (audio.info.length * 0.33) + 60
        if audio.info.length > l2:
            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
        else:
            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
        sendVoice(chat_id, "output.ogg")
    if content_type == "video":
        os.system("rm -f *.mp4")
        videofile = msg['video']
        fileid = msg['video']['file_id']
        flavor = telepot.flavor(msg)
        summary = telepot.glance(msg, flavor=flavor)
        print(flavor, summary)
        print(fileid)
        print(bot.getFile(file_id=fileid))
        filename = bot.getFile(file_id=fileid)['file_path']
        os.system("wget https://api.telegram.org/file/bot" + TOKEN + "/" + filename + " -O " + filename)
        os.system("ffmpeg -ss 0 -t 59 -y -i " + filename + " -strict -2 -c:v libx264 -crf 26 -vf scale=480:480 vm.mp4")
        sendVideoNote(chat_id, "vm.mp4")
    if content_type == "text":
        if msg['text'].startswith("/boxxy"):
            sendVoice(chat_id, "assets/boxxy.ogg")
        if msg['text'].startswith("/vid http://") or msg['text'].startswith("/vid https://"):
            try:
                message = bot.sendMessage(chat_id, "Downloading...")
                input_text = msg['text'].split("/vid ")[1]
                input_text = input_text.split('&')[0]
                msgid = telepot.message_identifier(message)
                os.system("rm -f *.mp4")
                cmd_download = "youtube-dl --geo-bypass -f mp4 -o video.%(ext)s " + input_text
                subprocess.Popen(cmd_download.split(), shell=False).wait()
                cmd_conv = "ffmpeg -y -i video.mp4 -c:v libx264 -crf 26 -vf scale=640:-1 -strict -2 out.mp4"
                bot.editMessageText(msgid, "Converting...")
                subprocess.Popen(cmd_conv.split(), shell=False).wait()
                filename = "out.mp4"
                os.system("ffmpeg -ss 0 -t 59 -y -i " + filename + " -strict -2 -c:v libx264 -crf 26 -vf scale=480:480 vm.mp4")
                bot.editMessageText(msgid, "Sending...")
                sendVideoNote(chat_id, "vm.mp4")
                f = open("out.mp4", "r")
                bot.sendVideo(chat_id, f)
                f.close()
                bot.deleteMessage(msgid)
                if chat_type == "private":
                    bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
                done = True
            except Exception, e:
                done = True
                f = open("errormsg.txt", "r")
                s = f.read()
                f.close()
                exc_type, exc_obj, tb = sys.exc_info()
                f = tb.tb_frame
                lineno = tb.tb_lineno
                error = str("line " + str(lineno) + ": " + str(e))
                url = msg["text"]
                chatid = str(chat_id)
                release = str(subprocess.check_output("git rev-parse --verify HEAD", shell=True)).replace("b'", "").replace("'", "").replace("\\n", "")
                s = s.replace("$crashlog$", error)
                s = s.replace("$message$", url)
                s = s.replace("$chatid$", chatid)
                s = s.replace("$release$", release)
                s = s.replace("$botowner$", BOTMASTER)
                s = s.replace("$bottag$", bottag)
                try:
                    bot.deleteMessage(msgid)
                    bot.sendMessage(chat_id, s, parse_mode="HTML")
                except:
                    bot.sendMessage(chat_id, s, parse_mode="HTML")
        try:
            os.system("rm -f audio.jpg")
            os.system("rm -f thumb.jpg")
        except:
            pass
        if msg['text'].startswith("/help") and not chat_type == "channel":
            f = open("help.txt", "r")
            s = f.read()
            f.close()
            s = s.replace("%bottag%", "@" + bottag).replace("%botmaster%", "@" + BOTMASTER)
            bot.sendMessage(chat_id, s, disable_web_page_preview=True)
        if msg['text'].startswith("/chatid"):
            bot.sendMessage(chat_id, "Your chat_id is: <pre>" + str(chat_id) + "</pre>", parse_mode="HTML")
        if msg['text'].startswith("/settag"):
            if chat_type == "channel":
                if msg['text'] == "/settag":
                    f = open("tags.txt","w+")
                    s = f.read().split("\n")
                    for line in s:
                        if not str(chat_id) in line:
                            f.write(line)
                    f.close()
                else:
                    try:
                        input_text = msg['text'].split("/settag @")[1]
                    except:
                        try:
                            input_text = msg['text'].split("/settag ")[1]
                        except:
                            pass
                    f = open("tags.txt","a")
                    f.write(str(chat_id) + ":" + input_text + "\n")
                    f.close()
        msgid = None
        try:
            input_text = msg['text']
            input_text = input_text.split('&')[0]
            if "group" in chat_type and "/conv" in input_text:
                goon = True
                input_text = input_text.replace("/conv", "").replace(" ", "")
            else:
                if "group" in chat_type:
                    goon = False
                else:
                    goon = True
            if goon == True and done == False:
                if not chat_type == "channel" and input_text.startswith("http"):
                    message = bot.sendMessage(chat_id, "Downloading...")
                    msgid = telepot.message_identifier(message)
                # Apparently some users are so dumb, that they forgot what an URL is
                # Thanks StackOverflow: https://stackoverflow.com/questions/839994/extracting-a-url-in-python
                try:
                    input_text = re.search("(?P<url>https?://[^\s]+)", input_text).group("url")
                except:
                    pass
                # Oh and please replace new lines, so the bot doesn't crash
                input_text = input_text.replace("\n", " ")
                f = open("tags.txt","r")
                s = f.read().split("\n")
                f.close()
                username = ""
                for line in s:
                    chanid = line.split(":")[0]
                    if chanid == str(chat_id):
                        username = line.split(":")[1]
                        username = "\n🆔 @" + username
                if "mixcloud" in input_text:
                    cmd = 'youtube-dl --add-metadata -v -x --audio-format mp3 --output audio.%%(ext)s ' + input_text
                    print(cmd)
                    subprocess.check_call(cmd.split(), shell=False)
                    r = requests.get(input_text)
                    c = r.content
                    title = c.split('<title>')[1].split('</title>')[0]
                    stitle = html.unescape(title.split(' by ')[0])
                    artist = html.unescape(title.split(' by ')[1].split(' | Mixcloud')[0].split(',')[0])
                    title = stitle
                    filename = artist.replace(" ", "-").replace("/", "-") + "_" + title.replace(" ", "-").replace("/", "-") + ".mp3"
                    cover = "https://thumbnailer.mixcloud.com/unsafe/800x800/extaudio/" + c.split('src="https://thumbnailer.mixcloud.com/unsafe/60x60/extaudio/')[1].split('"')[0]
                    os.system("wget -O audio.jpg \"" + cover + "\"")
                    if not chat_type == "channel":
                        bot.editMessageText(msgid, "Converting...")
                    os.system("lame -b 320 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                    audio = MP3("audio.mp3")
                    length = audio.info.length * 0.33
                    l2 = length + 60
                    if audio.info.length > l2:
                        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                    else:
                        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                    if not chat_type == "channel":
                        bot.editMessageText(msgid, "Sending...")
                    f = open("audio.jpg")
                    bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist + username)
                    f.close()
                    if os.path.exists("audio.jpg"):
                        os.system("convert audio.jpg -resize 90x90 thumb.jpg")
                    else:
                        os.system("convert blank.jpg -resize 90x90 thumb.jpg")
                    sendAudioChan(chat_id,"audio.mp3",artist,title,username,thumb)
                    f = open("output.ogg", "r")
                    bot.sendVoice(chat_id,f,username)
                    f.close()
                    if chat_type == "private":
                        bot.deleteMessage(msgid)
                        bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
                if "spotify" in input_text:
                    try:
                        trackid = input_text.replace("https://open.spotify.com/track/", "").split("?")[0]
                    except:
                        trackid = input_text.replace("https://open.spotify.com/track/", "")
                    print(trackid)
                    r = requests.get(input_text)
                    title = r.content.split('<title>')[1].split('</title>')[0]
                    stitle = html.unescape(title.split(',')[0])
                    artist = html.unescape(title.split(', a song by ')[1].split(' on Spotify')[0].split(',')[0])
                    if " (feat." in stitle:
                        stitle = stitle.split(' (')[0]
                    title = stitle
                    data = r.content.split('Spotify.Entity = ')[1].split(';')[0]
                    cover = data.split('"url":"')[1].split("\"")[0].replace("\\", "")
                    year = data.split('"release_date":"')[1].split('"')[0].split('-')[0]
                    albumtitle = data.split('"name":"')[2].split('"')[0].split('-')[0]
                    os.system("wget -O audio.jpg \"" + cover + "\"")
                    query = urllib.quote_plus(artist + " - " + title)
                    print(query)
                    cmd = "youtube-dl --geo-bypass --add-metadata -x --prefer-ffmpeg --extract-audio -v --audio-format mp3 --output \"audio.%%(ext)\" \"gvsearch1:" + query + "\""
                    subprocess.check_call(cmd, shell=True)
                    filename = artist.replace(" ", "-").replace("/", "-") + "_" + title.replace(" ", "-").replace("/", "-") + ".mp3"
                    if not chat_type == "channel":
                        bot.editMessageText(msgid, "Converting...")
                    os.system("lame -b 320 --ti audio.jpg  --ty " + year + " --tl \"" + albumtitle + "\" --tc @" + bottag + " --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                    audio = MP3(ucode(filename))
                    length = audio.info.length * 0.33
                    l2 = (audio.info.length * 0.33) + 60
                    if audio.info.length > l2:
                        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                    else:
                        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                    if not chat_type == "channel":
                        bot.editMessageText(msgid, "Sending...")
                    f = open("audio.jpg")
                    bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist + username)
                    f.close()
                    if os.path.exists("audio.jpg"):
                        os.system("convert audio.jpg -resize 90x90 thumb.jpg")
                    else:
                        os.system("convert blank.jpg -resize 90x90 thumb.jpg")
                    sendAudioChan(chat_id,filename,artist,title,username,thumb)
                    f = open("output.ogg", "r")
                    bot.sendVoice(chat_id,f,username)
                    f.close()
                    if chat_type == "private":
                        bot.deleteMessage(msgid)
                        bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
                if "soundcloud" in input_text:
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
                        os.system("wget \"" + track.artwork_url.replace("-large", "-crop") + "?t500x500\" -O raw_audio.jpg")
                        os.system("convert raw_audio.jpg -resize 800x800 audio.jpg")
                        os.system("rm -f raw_audio.jpg")
                        if not chat_type == "channel":
                            bot.editMessageText(msgid, "Converting...")
                        os.system("lame -b 320 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                    except:
                        printable = set(string.printable)
                        artist = filter(lambda x: x in printable, thist.user['username'])
                        printable = set(string.printable)
                        title = filter(lambda x: x in printable, thist.title)
                        os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                        try:
                            os.system("wget \"" + track.artwork_url.replace("-large", "-crop") + "?t500x500\" -O raw_audio.jpg")
                            os.system("convert raw_audio.jpg -resize 800x800 audio.jpg")
                        except:
                            pass
                        os.system("rm -f raw_audio.jpg")
                        if not chat_type == "channel":
                            bot.editMessageText(msgid, "Converting...")
                        try:
                            os.system("lame -b 320 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                        except:
                            os.system("lame -b 320 --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                    if not chat_type == "channel":
                        bot.editMessageText(msgid, "Sending...")
                    try:
                        f = open("audio.jpg")
                        bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist)
                        f.close()
                    except:
                        f = open("blank.jpg")
                        bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist)
                        f.close()
                    if os.path.exists("audio.jpg"):
                        os.system("convert audio.jpg -resize 90x90 thumb.jpg")
                    else:
                        os.system("convert blank.jpg -resize 90x90 thumb.jpg")
                    try:
                        sendAudioChan(chat_id, ucode(filename), ucode(artist), ucode(title), username, thumb)
                    except:
                        filename = "audio.mp3"
                        sendAudioChan(chat_id, ucode(filename), ucode(artist), ucode(title), username, thumb)
                    audio = MP3(ucode(filename))
                    length = audio.info.length * 0.33
                    l2 = length + 60
                    if audio.info.length > l2:
                        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                    else:
                        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                    f = open("output.ogg", "r")
                    bot.sendVoice(chat_id,f,username)
                    f.close()
                    if chat_type == "private":
                        bot.deleteMessage(msgid)
                        bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
                if "youtu" in input_text:
                    input_text = input_text.replace("music.", "")
                    cmd = 'youtube-dl --geo-bypass --add-metadata -x --prefer-ffmpeg --extract-audio -v --audio-format mp3 \
                        --output audio.%%(ext)s %summary'%(input_text)
                    subprocess.check_call(cmd.split(), shell=False)
                    tag = eyed3.load("audio.mp3")
                    try:
                        title = get_artist_title(tag.tag.title).split(" - ")[1]
                        artist = get_artist_title(tag.tag.title).split(" - ")[0]
                    except:
                        title = tag.tag.title.replace("\"", "")
                        artist = tag.tag.artist
                    try:
                        artist = artist.replace(" - Topic", "")
                    except:
                        pass
                    try:
                        os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                    except:
                        pass
                    try:
                        if not os.path.isfile("audio.jpg"):
                            proc = subprocess.Popen(['youtube-dl', '--list-thumbnails', input_text], stdout=subprocess.PIPE)
                            youtubedl_output, err = proc.communicate()
                            imgurl = re.search("(?P<url>https?://[^\s]+)", youtubedl_output).group('url')
                            r = requests.get(imgurl)
                            if r.status_code == 200:
                                with open('audio.jpg', 'wb') as file:
                                    for chunk in r.iter_content(1024):
                                        file.write(chunk)
                    except:
                        pass
                    if not chat_type == "channel":
                        bot.editMessageText(msgid, "Converting...")
                    subprocess.Popen(["lame", "-V", "0", "-b", "320", "--ti", "audio.jpg", "--tt", title, "--ta", artist , "audio.mp3"], shell=False).wait()
                    if not chat_type == "channel":
                        bot.editMessageText(msgid, "Sending...")
                    try:
                        f = open("audio.jpg")
                        bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist + username)
                        f.close()
                    except:
                        f = open("blank.jpg")
                        bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist + username)
                        f.close()
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
                                    pass
                    if os.path.exists("audio.jpg"):
                        os.system("convert audio.jpg -resize 90x90 thumb.jpg")
                    else:
                        os.system("convert blank.jpg -resize 90x90 thumb.jpg")
                    try:
                        sendAudioChan(chat_id,filename,artist,title,username,thumb)
                    except:
                        filename = "audio.mp3"
                        sendAudioChan(chat_id,filename,artist,title,username,thumb)
                    audio = eyed3.load(filename)
                    tt = audio.tag.title
                    artist = audio.tag.artist
                    ad = MP3(filename)
                    length = ad.info.length * 0.33
                    l2 = length + 60
                    if ad.info.length > l2:
                        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                    else:
                        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                    f = open("output.ogg", "r")
                    bot.sendVoice(chat_id,f,username)
                    f.close()
                    try:
                        bot.deleteMessage(msgid)
                    except:
                        pass
                    if chat_type == "private":
                        bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
        except Exception, e:
            if chat_type == "private":
                f = open("errormsg.txt", "r")
                s = f.read()
                f.close()
                exc_type, exc_obj, tb = sys.exc_info()
                f = tb.tb_frame
                lineno = tb.tb_lineno
                error = str("line " + str(lineno) + ": " + str(e))
                url = msg["text"]
                chatid = str(chat_id)
                release = str(subprocess.check_output("git rev-parse --verify HEAD", shell=True)).replace("b'", "").replace("'", "").replace("\\n", "")
                s = s.replace("$crashlog$", error)
                s = s.replace("$message$", url)
                s = s.replace("$chatid$", chatid)
                s = s.replace("$release$", release)
                s = s.replace("$botowner$", BOTMASTER)
                s = s.replace("$bottag$", bottag)
                try:
                    bot.deleteMessage(msgid)
                    bot.sendMessage(chat_id, s, parse_mode="HTML")
                except:
                    bot.sendMessage(chat_id, s, parse_mode="HTML")
        else:
            f = open("counters-disabled.txt", "r")
            s = f.read()
            f.close()
            if not chat_type == "channel" and not chat_type == "private" and not str(chat_id) in s:
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
                ping = os.popen("ping -c1 www.google.com").read().split("time=")[1].split(" ms")[0]
                bot.sendMessage(chat_id, "Pong! (" + ping + " ms)")
            if msg['text'].startswith("/start") and chat_type == "private":
                bot.sendMessage(chat_id,"Hello, please send me the URL from Soundcloud, YouTube and many more I have to convert :)")
            if msg['text'].startswith("/addextra"):
                try:
                    extraname = msg['text'].replace('/addextra ', '').replace(':', '').replace('#', '').split('\n')[0]
                    if chat_type == "private":
                        proceed = True
                        try:
                            f = open("extras/" + str(chat_id) + ".txt", "r")
                            s = f.read().split('\n')
                            f.close()
                            for x in s:
                                mid = x.split(':')[0]
                                ename = x.split(':')[1]
                                cid = x.split(':')[2]
                                if ename == extraname:
                                    proceed = False
                        except:
                            pass
                        if proceed == True:
                            f = open("extras/" + str(chat_id) + ".txt", "a+")
                            f.write(str(telepot.message_identifier(msg['reply_to_message'])) + ":" + extraname + ":" + str(chat_id) + "\n")
                            f.close()
                            f = open("extras/" + str(chat_id) + "-extralist.txt", "a")
                            f.write(extraname + "\r\n")
                            f.close()
                            bot.sendMessage(chat_id, "Extra added!", reply_to_message_id=str(telepot.message_identifier(msg)))
                        else:
                            bot.sendMessage(chat_id, "Extra already exists!", reply_to_message_id=str(telepot.message_identifier(msg)))
                    else:
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        msgfrom = str(msg['from']['username'])
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == msgfrom:
                                    isAdmin = True
                            except:
                                pass
                        if msgfrom == BOTMASTER:
                            isAdmin = True
                        if isAdmin == True:
                            if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                extraname = msg['text'].split('/addextra ')[1].replace(':', '').replace('#', '').split('\n')[0]
                                proceed = True
                                try:
                                    f = open("extras/" + str(chat_id) + ".txt", "r")
                                    s = f.read().split('\n')
                                    f.close()
                                    for x in s:
                                        mid = x.split(':')[0]
                                        ename = x.split(':')[1]
                                        cid = x.split(':')[2]
                                        if ename == extraname:
                                            proceed = False
                                except:
                                    pass
                                if proceed == True:
                                    f = open("extras/" + str(chat_id) + ".txt", "a+")
                                    f.write(str(telepot.message_identifier(msg['reply_to_message'])) + ":" + extraname + ":" + str(chat_id) + "\n")
                                    f.close()
                                    f = open("extras/" + str(chat_id) + "-extralist.txt", "a")
                                    f.write(extraname + "\r\n")
                                    f.close()
                                    bot.sendMessage(chat_id, "Extra added!", reply_to_message_id=str(telepot.message_identifier(msg)))
                                else:
                                    bot.sendMessage(chat_id, "Extra already exists!", reply_to_message_id=str(telepot.message_identifier(msg)))
                            else:
                                bot.sendMessage(chat_id, "Error: Permission denied while trying to add extra!")
                        else:
                            bot.sendMessage(chat_id, "Error: Permission denied while trying to add extra!")
                except:
                    bot.sendMessage(chat_id, "Message not a reply to a message or no name defined! Reply to a message with /addextra [name]", reply_to_message_id=str(telepot.message_identifier(msg)))
            if msg['text'].startswith('#') or msg['text'].startswith("/extra "):
                try:
                    if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                        if msg['text'].startswith("/extra "):
                            extraname = msg['text'].split('/extra ')[1].replace('#', '').split('\n')[0]
                        else:
                            extraname = msg['text'].split('#')[1].split('\n')[0]
                        f = open("extras/" + str(chat_id) + ".txt", "r")
                        s = f.read().split('\n')
                        f.close()
                        mid = None
                        try:
                            for x in s:
                                ename = x.split(':')[1]
                                if ename == extraname:
                                    mid = x.split(':')[0].split(', ')[1].replace(')', '')
                                    cid = x.split(':')[2]
                        except:
                            pass
                        try:
                            msga = bot.forwardMessage(chat_id, chat_id, int(mid))
                        except:
                            bot.sendMessage(chat_id, "Error: Extra not found!")
                        try:
                            # Some stuff is pretty tricky here. You shouldn't change the order here if this function isn't broken.
                            if "document" in str(msga):
                                fileid = msga['document']['file_id']
                                bot.sendDocument(chat_id, fileid, reply_to_message_id=str(telepot.message_identifier(msg)))
                            if "sticker" in str(msga):
                                fileid = msga['sticker']['file_id']
                                bot.sendSticker(chat_id, fileid, reply_to_message_id=str(telepot.message_identifier(msg)))
                            if "voice" in str(msga):
                                fileid = msga['voice']['file_id']
                                bot.sendVoice(chat_id, fileid, reply_to_message_id=str(telepot.message_identifier(msg)))
                            if "video_note" in str(msga):
                                fileid = msga['video_note']['file_id']
                                bot.sendVideoNote(chat_id, fileid, reply_to_message_id=str(telepot.message_identifier(msg)))
                            if "video" in str(msga):
                                fileid = msga['video']['file_id']
                                bot.sendVideo(chat_id, fileid, reply_to_message_id=str(telepot.message_identifier(msg)))
                            if "photo" in str(msga):
                                fileid = msga['photo'][0]['file_id']
                                bot.sendPhoto(chat_id, fileid, reply_to_message_id=str(telepot.message_identifier(msg)))
                            if "audio" in str(msga):
                                fileid = msga['audio']['file_id']
                                bot.sendAudio(chat_id, fileid, reply_to_message_id=str(telepot.message_identifier(msg)))
                            if "file" in str(msga):
                                fileid = msga['document']['file_id']
                                bot.sendDocument(chat_id, fileid, reply_to_message_id=str(telepot.message_identifier(msg)))
                            if "text" in str(msga):
                                bot.sendMessage(chat_id, msga['text'], reply_to_message_id=str(telepot.message_identifier(msg)))
                        except:
                            pass
                        try:
                            bot.deleteMessage(telepot.message_identifier(msga))
                        except:
                            pass
                except:
                    bot.sendMessage(chat_id, "Error: Extra not found!")
            if msg['text'].startswith("/extralist") or msg['text'].startswith("/extras"):
                try:
                    if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                        f = open("extras/" + str(chat_id) + "-extralist.txt", "r")
                        bot.sendDocument(chat_id, f, reply_to_message_id=str(telepot.message_identifier(msg)))
                        f.close()
                except:
                    bot.sendMessage(chat_id, "Error: No extras available!")
            if msg['text'].startswith("/delextra"):
                if " " in msg['text']:
                    extraname = msg['text'].split('/delextra ')[1].replace('#', '').split('\n')[0]
                    if chat_type == "private":
                        f = open("extras/" + str(chat_id) + ".txt", "r")
                        lines = f.readlines()
                        f.close()
                        f = open("extras/" + str(chat_id) + ".txt", "w")
                        actuallyDidIt = False
                        for line in lines:
                            if not line.split(':')[1] == extraname:
                                f.write(line)
                        f.close()
                        f = open("extras/" + str(chat_id) + "-extralist.txt", "r")
                        linesb = f.readlines()
                        f.close()
                        f = open("extras/" + str(chat_id) + "-extralist.txt", "w")
                        for line in linesb:
                            if not line == extraname+"\r\n":
                                f.write(line)
                            else:
                                actuallyDidIt = True
                        f.close()
                        if actuallyDidIt == True:
                            bot.sendMessage(chat_id, "Success: Extra deleted!")
                        else:
                            bot.sendMessage(chat_id, "Error: Extra doesn't exist.")
                    if not chat_type == "private":
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        msgfrom = str(msg['from']['username'])
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == msgfrom:
                                    isAdmin = True
                            except:
                                pass
                        if msgfrom == BOTMASTER:
                            isAdmin = True
                        if isAdmin == True:
                            if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                f = open("extras/" + str(chat_id) + ".txt", "r")
                                lines = f.readlines()
                                f.close()
                                f = open("extras/" + str(chat_id) + ".txt", "w")
                                actuallyDidIt = False
                                for line in lines:
                                    if not line.split(':')[1] == extraname:
                                        f.write(line)
                                f.close()
                                f = open("extras/" + str(chat_id) + "-extralist.txt", "r")
                                linesb = f.readlines()
                                f.close()
                                f = open("extras/" + str(chat_id) + "-extralist.txt", "w")
                                for line in linesb:
                                    if not line == extraname+"\r\n":
                                        f.write(line)
                                    else:
                                        actuallyDidIt = True
                                f.close()
                                if actuallyDidIt == True:
                                    bot.sendMessage(chat_id, "Success: Extra deleted!")
                                else:
                                    bot.sendMessage(chat_id, "Error: Extra doesn't exist.")
                            else:
                                bot.sendMessage(chat_id, "Error: Permission denied while trying to delete extra!")
                        else:
                            bot.sendMessage(chat_id, "Error: Permission denied while trying to delete extra!")
                else:
                    bot.sendMessage(chat_id, "Error: Missing parameter!")
            if not chat_type == "private" and msg["text"].startswith("/disableextras"):
                admins = bot.getChatAdministrators(chat_id)
                isAdmin = False
                msgfrom = str(msg['from']['username'])
                for user in admins:
                    try:
                        if str(user['user']['username']).replace("u'", "").replace("'", "") == msgfrom:
                            isAdmin = True
                    except:
                        pass
                if msgfrom == BOTMASTER:
                    isAdmin = True
                if isAdmin == True:
                    os.system("touch extras/" + str(chat_id) + "-deactivated.txt")
                    bot.sendMessage(chat_id, "Extras disabled!")
            if not chat_type == "private" and msg["text"].startswith("/enableextras"):
                admins = bot.getChatAdministrators(chat_id)
                isAdmin = False
                msgfrom = str(msg['from']['username'])
                for user in admins:
                    try:
                        if str(user['user']['username']).replace("u'", "").replace("'", "") == msgfrom:
                            isAdmin = True
                    except:
                        pass
                if msgfrom == BOTMASTER:
                    isAdmin = True
                if isAdmin == True:
                    os.system("rm -f extras/" + str(chat_id) + "-deactivated.txt")
                    bot.sendMessage(chat_id, "Extras enabled!")
            if not chat_type == "private" and msg['text'].startswith("/disablecounters"):
                admins = bot.getChatAdministrators(chat_id)
                isAdmin = False
                msgfrom = str(msg['from']['username'])
                for user in admins:
                    try:
                        if str(user['user']['username']).replace("u'", "").replace("'", "") == msgfrom:
                            isAdmin = True
                    except:
                        pass
                if msgfrom == BOTMASTER:
                    isAdmin = True
                if isAdmin == True:
                    f = open("counters-disabled.txt", "a+")
                    f.write(str(chat_id) + "\n")
                    f.close()
                    bot.sendMessage(chat_id, "Success: Counters disabled")
            if not chat_type == "private" and msg['text'].startswith("/enablecounters"):
                admins = bot.getChatAdministrators(chat_id)
                isAdmin = False
                msgfrom = msg['from']['username']
                for user in admins:
                    try:
                        if str(user['user']['username']).replace("u'", "").replace("'", "") == msgfrom:
                            isAdmin = True
                    except:
                        pass
                if msgfrom == BOTMASTER:
                    isAdmin = True
                if isAdmin == True:
                    f = open("counters-disabled.txt", "r")
                    s = f.readlines()
                    f.close()
                    f = open("counters-disabled.txt", "w")
                    for x in s:
                        if not x == str(chat_id)+"\n":
                            f.write(x)
                    f.close()
                    bot.sendMessage(chat_id, "Success: Counters enabled!")

def sendAudio(chat_id,file_name,performer,title,thumb):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb'), 'thumb': open(thumb, 'rb')}
    data = {'chat_id' : chat_id, 'performer' : performer, 'title' : title}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendVideoNote(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendVideoNote"%(TOKEN)
    files = {'video_note': open(file_name, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendAudio2(chat_id,file_name,thumb):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb'), 'thumb': open(thumb, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendAudioChan(chat_id,file_name,performer,title,caption,thumb):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb'), 'thumb': open(thumb, 'rb')}
    data = {'chat_id' : chat_id, 'performer' : performer, 'title' : title, 'caption' : caption}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendVoice(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendVoice"%(TOKEN)
    files = {'voice': open(file_name, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def ucode(text):
    return text.decode().encode('utf-8')

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening ...')

while 1:
    time.sleep(10)
