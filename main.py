#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import telepot
import requests
import os
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
from moviepy.editor import VideoFileClip

reload(sys)
sys.setdefaultencoding("utf-8")

client = soundcloud.Client(client_id='LBCcHmRB8XSStWL6wKH2HPACspQlXg2P')
API_KEY = "9d3ee2a574eb3bb2a6f0a4e108e46ceb"
API_SECRET = "f982de3bd2d8e7ffe5c117b568b1fc3e"
lastfm = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

if 'BOTTAG' in os.environ:
    bottag = os.environ.get('BOTTAG')
else:
    bottag = "@keverythingbot"

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = ""
f = open("random.txt", "w+")
f.write(str(random.randint(20,30)))
f.close()
bottag = bottag.replace("@", "")

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
        video = VideoFileClip(filename)
        length = video.duration * 0.33
        l2 = (video.duration * 0.33) + 60
        if video.duration > l2:
            os.system("ffmpeg -ss " + str(length) + " -t 59 -y -i " + filename + " -strict -2 -c:v libx264 -crf 26 -vf scale=640:-1 vm.mp4")
        else:
            os.system("ffmpeg -ss 0 -t 59 -y -i " + filename + " -strict -2 -c:v libx264 -crf 26 -vf scale=640:-1 vm.mp4")
        f = open("vm.mp4", "r")
        bot.sendVideoNote(chat_id, f)
        f.close()
    if content_type == "text":
        os.system("rm -f audio.jpg")
        if msg['text'].startswith("/chatid"):
            bot.sendMessage(chat_id, "Your chat_id is: `" + str(chat_id) + "`", "Markdown")
        if msg['text'].startswith("/settag"):
            if chat_type == "channel":
                if msg['text'] == "/settag":
                    f = open("tags.txt","w+")
                    s = f.read().split("\n")
                    for line in s:
                        if not str(chat_id) in line:
                            f.write(line + "\n")
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
        if chat_type == "channel":
            input_text = msg['text']
            input_text = input_text.split('&')[0]
            f = open("tags.txt","r")
            s = f.read().split("\n")
            f.close()
            username = ""
            for line in s:
                chanid = line.split(":")[0]
                if chanid == str(chat_id):
                    username = line.split(":")[1]
                    username = "\n🆔 @" + username
            if input_text.startswith("http"):
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
                    try:
                        f = open("audio.jpg")
                        bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist + username)
                        f.close()
                    except:
                        f = open("blank.jpg")
                        bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist + username)
                        f.close()
                    print(filename)
                    sendAudioChan(chat_id,filename,artist,title,username)
                    audio = MP3(filename)
                    length = audio.info.length * 0.33
                    l2 = length + 60
                    if audio.info.length > l2:
                        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    else:
                        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    f = open("output.ogg", "r")
                    bot.sendVoice(chat_id,f,username)
                    f.close()
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
                        sendAudioChan(chat_id,filename,artist,title,username)
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
                        f = open("output.ogg", "r")
                        bot.sendVoice(chat_id,f,username)
                        f.close()
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
        if msg['text'].startswith("/video http://") or msg['text'].startswith("/video https://") and not chat_type == "channel":
            try:
                message = bot.sendMessage(chat_id, "Downloading...")
                input_text = msg['text'].split("/video ")[1]
                input_text = input_text.split('&')[0]
                msgid = telepot.message_identifier(message)
                os.system("rm -f *.mp4")
                cmd_download = "youtube-dl -f mp4 -o video.%(ext)s " + input_text
                subprocess.Popen(cmd_download.split(), shell=False).wait()
                cmd_conv = "ffmpeg -y -i video.mp4 -c:v libx264 -crf 26 -vf scale=640:-1 -strict -2 out.mp4"
                bot.editMessageText(msgid, "Converting...")
                subprocess.Popen(cmd_conv.split(), shell=False).wait()
                filename = "out.mp4"
                video = VideoFileClip(filename)
                length = video.duration * 0.33
                l2 = (video.duration * 0.33) + 60
                if video.duration > l2:
                    os.system("ffmpeg -ss " + str(length) + " -t 59 -y -i " + filename + " -strict -2 -c:v libx264 -crf 26 -vf scale=640:-1 vm.mp4")
                else:
                    os.system("ffmpeg -ss 0 -t 59 -y -i " + filename + " -strict -2 -c:v libx264 -crf 26 -vf scale=640:-1 vm.mp4")
                f = open("vm.mp4", "r")
                bot.sendVideoNote(chat_id, f)
                f.close()
                f = open("out.mp4", "r")
                bot.sendVideo(chat_id, f)
                f.close()
                bot.deleteMessage(msgid)
                bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
            except:
                try:
                    bot.editMessageText(msgid, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
                except:
                    bot.sendMessage(chat_id, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
        if msg['text'].startswith("/conv http://") or msg['text'].startswith("/conv https://") and not chat_type == "channel":
            try:
                message = bot.sendMessage(chat_id, "Downloading...")
                input_text = msg['text'].split("/conv ")[1]
                input_text = input_text.split('&')[0]
                msgid = telepot.message_identifier(message)
                if "soundcloud" in input_text:
                    track = client.get('/resolve', url=input_text)
                    thist = track
                    stream_url = client.get(thist.stream_url, allow_redirects=False)
                    artist = None
                    title = None
                    filename = u' '.join((thist.title.replace(" ", "_").replace("!", "_").replace("&", "_").replace("?", "_"), ".mp3")).encode('utf-8').strip()
                    try:
                        printable = set(string.printable)
                        artist = filter(lambda x: x in printable, thist.title.split(" - ")[0])
                        printable = set(string.printable)
                        title = filter(lambda x: x in printable, thist.title.split(" - ")[1])
                        os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                        os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                        year = ""
                        albumtitle = ""
                        try:
                            track = client.get('/tracks', q=artist + " " + title)[0]
                            year = track.created_at.split('/')[0]
                        except:
                            year = ""

                        album = lastfm.get_album(artist, lastfm.get_track(artist, title).get_album())
                        try:
                            albumtitle = str(album.title).split(" / ")[1]
                        except:
                            try:
                                albumtitle = str(album.title).split(" - ")[1]
                            except:
                                albumtitle = str(album.title)
                        bot.editMessageText(msgid, "Converting...")
                        os.system("lame -V0 --ti audio.jpg  --ty " + year + " --tl \"" + albumtitle + "\" --tc @" + bottag + " --tc @" + bottag + " --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                    except:
                        printable = set(string.printable)
                        artist = filter(lambda x: x in printable, thist.user['username'])
                        printable = set(string.printable)
                        title = filter(lambda x: x in printable, thist.title)
                        os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                        os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                        try:
                            try:
                                track = client.get('/tracks', q=artist + " " + title)[0]
                                year = track.created_at.split('/')[0]
                            except:
                                year = ""

                            album = lastfm.get_album(artist, lastfm.get_track(artist, title).get_album())
                            try:
                                albumtitle = str(album.title).split(" / ")[1]
                            except:
                                try:
                                    albumtitle = str(album.title).split(" - ")[1]
                                except:
                                    albumtitle = str(album.title)
                            bot.editMessageText(msgid, "Converting...")
                            subprocess.Popen(["lame", "-V", "0", "-b", "320", "--ty", year, "--tl", albumtitle, "--ti", "audio.jpg", "--tc", "@" + bottag, "--tt", title, "--ta", artist , "audio.mp3"], shell=False).wait()
                        except:
                            pass
                    bot.editMessageText(msgid, "Sending...")
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
                    bot.deleteMessage(msgid)
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
                        os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                        try:
                            try:
                                track = client.get('/tracks', q=artist + " " + title)[0]
                                year = track.created_at.split('/')[0]
                            except:
                                year = ""

                            album = lastfm.get_album(artist, lastfm.get_track(artist, title).get_album())
                            try:
                                albumtitle = str(album.title).split(" / ")[1]
                            except:
                                try:
                                    albumtitle = str(album.title).split(" - ")[1]
                                except:
                                    albumtitle = str(album.title)
                            bot.editMessageText(msgid, "Converting...")
                            subprocess.Popen(["lame", "-V", "0", "-b", "320", "--ty", year, "--tl", albumtitle, "--ti", "audio.jpg", "--tc", "@" + bottag, "--tt", title, "--ta", artist , "audio.mp3"], shell=False).wait()
                        except:
                            pass
                        bot.editMessageText(msgid, "Sending...")
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
                        audio = eyed3.load(filename)
                        tt = audio.tag.title
                        artist = audio.tag.artist
                        ad = MP3(filename)
                        length = ad.info.length * 0.33
                        l2 = length + 60
                        if ad.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                        sendVoice(chat_id, "output.ogg")
                        bot.deleteMessage(msgid)
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
            except:
                try:
                    bot.editMessageText(msgid, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
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
                msgid = None
                try:
                    message = bot.sendMessage(chat_id, "Downloading...")
                    msgid = telepot.message_identifier(message)
                    input_text = msg['text']
                    input_text = input_text.split('&')[0]
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
                            os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                            bot.editMessageText(msgid, "Converting...")
                            os.system("lame -V0 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                        except:
                            printable = set(string.printable)
                            artist = filter(lambda x: x in printable, thist.user['username'])
                            printable = set(string.printable)
                            title = filter(lambda x: x in printable, thist.title)
                            os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                            os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                            bot.editMessageText(msgid, "Converting...")
                            os.system("lame -V0 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                        bot.editMessageText(msgid, "Sending...")
                        try:
                            f = open("audio.jpg")
                            bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist)
                            f.close()
                        except:
                            f = open("blank.jpg")
                            bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist)
                            f.close()
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
                        bot.deleteMessage(msgid)
                        bot.sendMessage(chat_id,"Here you go!")
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
                            os.system("sacad \"" + artist + "\" \"" + title + "\" 800 audio.jpg")
                            try:
                                try:
                                    track = client.get('/tracks', q=artist + " " + title)[0]
                                    year = track.created_at.split('/')[0]
                                except:
                                    year = ""

                                album = lastfm.get_album(artist, lastfm.get_track(artist, title).get_album())
                                try:
                                    albumtitle = str(album.title).split(" / ")[1]
                                except:
                                    try:
                                        albumtitle = str(album.title).split(" - ")[1]
                                    except:
                                        albumtitle = str(album.title)
                                bot.editMessageText(msgid, "Converting...")
                                subprocess.Popen(["lame", "-V", "0", "-b", "320", "--ty", year, "--tl", albumtitle, "--ti", "audio.jpg", "--tc", "@" + bottag, "--tt", title, "--ta", artist , "audio.mp3"], shell=False).wait()
                            except:
                                pass
                            bot.editMessageText(msgid, "Sending...")
                            try:
                                f = open("audio.jpg")
                                bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist)
                                f.close()
                            except:
                                f = open("blank.jpg")
                                bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist)
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
                                            bot.sendMessage(chat_id, "Uh-oh, something miserably bad happened. Contact @Sommerlichter, he might fix this.")
                            sendAudio(chat_id, filename, artist, title)
                            audio = eyed3.load(filename)
                            tt = audio.tag.title
                            artist = audio.tag.artist
                            ad = MP3(filename)
                            length = ad.info.length * 0.33
                            l2 = length + 60
                            if ad.info.length > l2:
                                os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                            else:
                                os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                            sendVoice(chat_id, "output.ogg")
                            bot.deleteMessage(msgid)
                            bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
                        else:
                            url = msg['text']
                            filename = subprocess.check_output(["node", "--no-warnings", "download-url.js", url]).split('\n')[0]
                            bot.editMessageText(msgid, "Converting...")
                            os.system("ffmpeg -y -i \"" + filename + "\" -codec:a libmp3lame -qscale:a 0 -map_metadata 0:g output.mp3")
                            bot.editMessageText(msgid, "Sending...")
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
                            bot.deleteMessage(msgid)
                            bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
                except:
                    try:
                        bot.editMessageText(msgid, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
                    except:
                        bot.sendMessage(chat_id, "Oh no, something bad happened! Please contact @Sommerlichter and include your URL and other relevant information in your request.")
            if chat_type == "private" and not msg['text'].startswith("/start") and not msg['text'].startswith("/ping") and not msg['text'].startswith("/video") and not msg['text'].startswith("http") and not msg['text'].startswith("/conv"):
                try:
                    msgid = None
                    message = bot.sendMessage(chat_id, "Downloading...")
                    msgid = telepot.message_identifier(message)
                    input_text = msg['text']
                    url = subprocess.check_output(["node", "--no-warnings", "download.js", input_text]).split('\n')[0]
                    filename = subprocess.check_output(["node", "--no-warnings", "download-url.js", url]).split('\n')[0]
                    fname = filename
                    bot.editMessageText(msgid, "Converting...")
                    os.system("ffmpeg -y -i \"" + filename + "\" -codec:a libmp3lame -qscale:a 0 -map_metadata 0:g output.mp3")
                    bot.editMessageText(msgid, "Sending...")
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
                    bot.deleteMessage(msgid)
                    bot.sendMessage(chat_id,"Here you go!\nCheck out @everythingbots for news and informations about this bot.",disable_web_page_preview=True)
                except:
                    try:
                        bot.editMessageText(msgid, "I cannot find the song you're looking for. Go find yourself a link and enter it here, so I know where to start from.")
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

def sendAudioChan(chat_id,file_name,performer,title,caption):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'performer' : performer, 'title' : title, 'caption' : caption}
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
