#!/usr/bin/python3

import sys
import time
import os
import os.path
import re
import subprocess
import time
import eyed3
import random
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import soundcloud
import string
import json
import urllib.request
import html.parser
import logging
import telegram
import requests
from telegram.error import NetworkError, Unauthorized


update_id = None

client = soundcloud.Client(client_id='LBCcHmRB8XSStWL6wKH2HPACspQlXg2P')
thumb = "thumb.jpg"

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = ""
if 'BOTMASTER' in os.environ:
    BOTMASTER = os.environ.get('BOTMASTER')
else:
    BOTMASTER = 'bubblineyuri'
f = open("random.txt", "w+")
f.write(str(random.randint(10,30)))
f.close()

# Initializing APIs
client = soundcloud.Client(client_id='LBCcHmRB8XSStWL6wKH2HPACspQlXg2P')
thumb = "thumb.jpg"

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = ""
if 'BOTMASTER' in os.environ:
    BOTMASTER = os.environ.get('BOTMASTER')
else:
    BOTMASTER = 'Sommerlichter'
if 'ALLOWUNSUBS' in os.environ:
    ALLOWUNSUBS = os.environ.get('ALLOWUNSUBS')
else:
    ALLOWUNSUBS = 'TRUE'
if 'MODULES' in os.environ:
    MODULES = os.environ.get('MODULES')
else:
    MODULES = 'spotify,youtube,soundcloud,mixcloud,voice,videonotes,counters,extras,help,stats,commands,subscriptions,videos,boxxy,settag,ping'
f = open("random.txt", "w+")
f.write(str(random.randint(10,30)))
f.close()

def isenabled(module):
    modenabled = False
    for x in MODULES.split(','):
        if x == module:
            modenabled = True
    return modenabled

def handle(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:
            os.system("sh clean.sh")
            done = False
            bottag = bot.getMe()["username"]
            f = open("random.txt", "r")
            rnumber = int(f.read())
            f.close()
            chat_type = update.message.chat.type
            chat_id = update.message.chat_id
            if chat_type == "private" or "group" in chat_type:
                try:
                    if chat_type == "private":
                        f = open("chatids.txt", "r")
                    else:
                        f = open("chatids2.txt", "r")
                    x = f.read()
                    f.close()
                    f = open("subsoff.txt", "r")
                    y = f.read()
                    f.close()
                    if not str(chat_id) in x:
                        try:
                            if chat_type == "private":
                                f = open("chatids.txt", "a+")
                            else:
                                f = open("chatids2.txt", "a+")
                            f.write(str(chat_id) + ":" + update.message.from_user.username + "\n")
                            f.close()
                        except:
                            if chat_type == "private":
                                f = open("chatids.txt", "a+")
                            else:
                                f = open("chatids2.txt", "a+")
                            f.write(str(chat_id) + "\n")
                            f.close()
                    if str(chat_id) in y:
                        lines = y.split("\n")
                        if chat_type == "private":
                            f = open("chatids.txt", "w")
                        else:
                            f = open("chatids2.txt", "w")
                        for line in lines:
                            if not str(chat_id) in line:
                                f.write(line)
                        f.close()
                except:
                    pass
            if update.message.audio:
                fileid = update.message.audio.file_id
                print(fileid)
                getfile = bot.get_file(fileid).download()
                filename = getfile
                if ".mp3" in filename:
                    audio = MP3(filename)
                    length = audio.info.length * 0.33
                    l2 = (audio.info.length * 0.33) + 60
                if ".m4a" in filename:
                    audio = MP4(filename)
                    length = audio.info.length * 0.33
                    l2 = (audio.info.length * 0.33) + 60
                if audio.info.length > l2:
                    os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 output.ogg")
                else:
                    os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 output.ogg")
                sendVoice(update.message.chat_id, "output.ogg","")
            if update.message.video:
                fileid = update.message.video.file_id
                print(fileid)
                print(bot.getFile(file_id=fileid))
                filename = bot.getFile(file_id=fileid)['file_path']
                os.system("wget https://api.telegram.org/file/bot" + TOKEN + "/" + filename + " -O " + filename)
                os.system("ffmpeg -ss 0 -t 59 -y -i " + filename + " -strict -2 -c:v libx264 -crf 26 -vf scale=480:480 vm.mp4")
                sendVideoNote(chat_id, "vm.mp4")
            if update.message.text:
                if update.message["text"].startswith("/stats"):
                    f = open("templates/stats")
                    s = f.read()
                    f.close()
                    err_nope = "not applicable"
                    err_disabled = "disabled"
                    err_unset = "not set"
                    ###
                    s = s.replace("%%chat_id%%", str(chat_id))
                    if chat_type == "channel":
                        f = open("tags.txt","r")
                        s = f.read().split("\n")
                        f.close()
                        username = ""
                        for line in s:
                            chanid = line.split(":")[0]
                            if chanid == str(chat_id):
                                username = line.split(":")[1]
                        if not username == "":
                            s = s.replace("%%channel_id%%", username)
                        else:
                            s = s.replace("%%channel_id%%", err_unset)
                    else:
                        if isenabled("settag"):
                            s = s.replace("%%channel_id%%", err_nope)
                        else:
                            s = s.replace("%%channel_id%%", err_disabled)
                    if chat_type == "private" or "group" in chat_type:
                        f = open("chatids.txt", "r")
                        cids = f.read()
                        f.close()
                        f = open("chatids2.txt", "r")
                        cids = cids + f.read()
                        f.close()
                        if str(chat_id) in cids:
                            s = s.replace("%%subscribed%%", "yes")
                        else:
                            s = s.replace("%%subscribed%%", "no")
                    else:
                        if isenabled("subscriptions"):
                            s = s.replace("%%subscribed%%", err_nope)
                        else:
                            s = s.replace("%%subscribed%%", err_disabled)
                    if "group" in chat_type:
                        f = open("counters-disabled.txt")
                        x = f.read()
                        f.close()
                        if isenabled("counters"):
                            if str(chat_id) in x:
                                s = s.replace("%%counters%%", "deactivated")
                            else:
                                s = s.replace("%%counters%%", "activated")
                        else:
                            s = s.replace("%%counters%%", err_disabled)
                    else:
                        if isenabled("counters"):
                            s = s.replace("%%counters%%", err_nope)
                        else:
                            s = s.replace("%%counters%%", err_disabled)
                    if "group" in chat_type or chat_type == "channel":
                        if isenabled("extras"):
                            if os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                s = s.replace("%%extras%%", "deactivated")
                            else:
                                s = s.replace("%%extras%%", "activated")
                        else:
                            s = s.replace("%%extras%%", err_disabled)
                    else:
                        s = s.replace("%%extras%%", err_nope)
                    s = s.replace("%%chat_type%%", chat_type)
                    s = s.replace("%%modules%%", MODULES.replace(",", ", "))
                    bot.sendMessage(chat_id, s, parse_mode="HTML")
                if update.message["text"].startswith("/unsub") and isenabled("subscriptions"):
                    if ALLOWUNSUBS == 'TRUE':
                        if chat_type == "private" or "group" in chat_type:
                            proceed = False
                            if "group" in chat_type:
                                admins = bot.getChatAdministrators(chat_id)
                                isAdmin = False
                                for user in admins:
                                    try:
                                        if str(user['user']['username']).replace("u'", "").replace("'", "") == update.message.from_user.username:
                                            isAdmin = True
                                    except:
                                        pass
                                if update.message.from_user.username == BOTMASTER:
                                    isAdmin = True
                                if isAdmin == True:
                                    proceed = True
                            else:
                                proceed = True
                            if proceed == True:
                                f = open("subsoff.txt", "a")
                                f.write(str(chat_id) + "\n")
                                f.close()
                                f = open("subsoff.txt", "r")
                                lines = f.readlines()
                                f.close()
                                if chat_type == "private":
                                    f = open("chatids.txt", "w")
                                else:
                                    f = open("chatids2.txt", "w")
                                for line in lines:
                                    if not str(chat_id) in line:
                                        f.write(line)
                                f.close()
                                bot.sendMessage(chat_id, "Success: Unsubscribed!")
                    else:
                        bot.sendMessage(chat_id, "My bot owner doesn't allow me to unsubscribe :(")
                if update.message["text"].startswith("/sub") and isenabled("subscriptions"):
                    if chat_type == "private" or "group" in chat_type:
                        proceed = False
                        if "group" in chat_type:
                            admins = bot.getChatAdministrators(chat_id)
                            isAdmin = False
                            for user in admins:
                                try:
                                    if str(user['user']['username']).replace("u'", "").replace("'", "") == update.message.from_user.username:
                                        isAdmin = True
                                except:
                                    pass
                            if update.message.from_user.username == BOTMASTER:
                                isAdmin = True
                            if isAdmin == True:
                                proceed = True
                        else:
                            proceed = True
                        if proceed == True:
                            f = open("subsoff.txt", "r")
                            lines = f.readlines()
                            f.close()
                            f = open("subsoff.txt", "w")
                            for line in lines:
                                if not line == str(chat_id)+"\n":
                                    f.write(line)
                            f.close()
                            try:
                                if chat_type == "private":
                                    f = open("chatids.txt", "a+")
                                else:
                                    f = open("chatids2.txt", "a+")
                                f.write(str(chat_id) + ":" + update.message["from"]["username"] + "\n")
                                f.close()
                            except:
                                if chat_type == "private":
                                    f = open("chatids.txt", "a+")
                                else:
                                    f = open("chatids2.txt", "a+")
                                f.write(str(chat_id) + "\n")
                                f.close()
                            bot.sendMessage(chat_id, "Success: Subscribed!")
                if update.message['text'].startswith("/boxxy") and isenabled("boxxy"):
                    sendVoice(chat_id, "assets/boxxy.ogg","")
                if update.message['text'].startswith("/vid http://") or update.message['text'].startswith("/vid https://"):
                    if isenabled("videos"):
                        try:
                            status_message = bot.sendMessage(chat_id, "Downloading...")
                            input_text = update.message['text'].split("/vid ")[1]
                            input_text = input_text.split('&')[0]
                            cmd_download = ["youtube-dl", "--no-continue", "-f", "mp4", "-o", "video.%(ext)s", input_text]
                            subprocess.Popen(cmd_download, shell=False).wait()
                            cmd_conv = "ffmpeg -y -i video.mp4 -vcodec libx264 -crf 27 -preset veryfast -c:a copy -s 640x360 out.mp4"
                            bot.editMessageText(update.messageid, "Converting...")
                            subprocess.Popen(cmd_conv.split(' '), shell=False).wait()
                            filename = "out.mp4"
                            subprocess.Popen(str("ffmpeg -ss 0 -t 59 -y -i " + filename + " -vcodec libx264 -crf 27 -preset veryfast -c:a copy -s 480x480 vm.mp4").split(' '), shell=False).wait()
                            bot.editMessageText(update.messageid, "Sending...")
                            sendVideoNote(chat_id, "vm.mp4")
                            f = open("out.mp4", "r")
                            bot.sendVideo(chat_id, f)
                            f.close()
                            try:
                                bot.deleteMessage(update.messageid)
                                bot.deleteMessage(telepot.message_identifier(update.message))
                            except:
                                pass
                            if chat_type == "private":
                                bot.sendMessage(chat_id,"Here you go!\nCheck out @kseverythingbot_army for news and informations about this bot.",disable_web_page_preview=True)
                            done = True
                        except Exception as e:
                            if chat_type == "private":
                                f = open("templates/error", "r")
                                s = f.read()
                                f.close()
                                exc_type, exc_obj, tb = sys.exc_info()
                                print(exc_type, exc_obj, tb)
                                f = tb.tb_frame
                                lineno = tb.tb_lineno
                                error = str("line " + str(lineno) + ": " + str(e))
                                url = update.message["text"]
                                chatid = str(chat_id)
                                release = str(subprocess.check_output("git rev-parse --verify HEAD", shell=True)).replace("b'", "").replace("'", "").replace("\\n", "")
                                s = s.replace("%%crashlog%%", error)
                                s = s.replace("%%message%%", url)
                                s = s.replace("%%chatid%%", chatid)
                                s = s.replace("%%release%%", release)
                                s = s.replace("%%bottag%%", bottag)
                                try:
                                    bot.deleteMessage(update.message.id)
                                    bot.sendMessage(chat_id, "<pre>An error occured. It has been reported to my owner.</pre>", parse_mode="HTML")
                                except:
                                    bot.sendMessage(chat_id, "<pre>An error occured. It has been reported to my owner.</pre>", parse_mode="HTML")
                                try:
                                    f = open("chatids.txt")
                                    c = f.readlines()
                                    f.close()
                                    master = ""
                                    for x in c:
                                        if BOTMASTER in x:
                                            master = x.split(":")[0]
                                    bot.sendMessage(master, s, parse_mode="HTML")
                                except:
                                    pass
                try:
                    os.system("rm -f audio.jpg")
                    os.system("rm -f thumb.jpg")
                except:
                    pass
                if update.message['text'].startswith("/help") or update.message['text'].startswith("/commands"):
                    proceed = False
                    if update.message['text'].startswith("/commands" ) and isenabled("commands"):
                        proceed = True
                        f = open("templates/commands", "r")
                        s = f.read()
                        f.close()
                    if update.message['text'].startswith("/help") and isenabled("help"):
                        proceed = True
                        f = open("templates/help", "r")
                        s = f.read()
                        f.close()
                        release = str(subprocess.check_output("git rev-parse --verify HEAD", shell=True)).replace("b'", "").replace("'", "").replace("\\n", "")
                        s = s.replace("%%bottag%%", "@" + bottag).replace("%%botmaster%%", "@" + BOTMASTER).replace("%%release%%", release)
                    if "group" in chat_type and proceed:
                        f = open("chatids.txt", "r")
                        cids = f.read()
                        f.close()
                        f = open("subsoff.txt", "r")
                        cids = cids + f.read()
                        f.close()
                        if update.message.from_user.username in cids:
                            cid = 0
                            try:
                                for x in cids.split("\n"):
                                    if x.split(":")[1] == update.message.from_user.username:
                                        cid = int(x.split(":")[0])
                            except:
                                pass
                            bot.sendMessage(cid, s, disable_web_page_preview=True, parse_mode="HTML")
                            status_message = bot.sendMessage(chat_id, "Hey @" + update.message.from_user.username + "! I've sent you the help via private message.")
                            time.sleep(5)
                            bot.deleteMessage(chat_id, status_message.message_id)
                            try:
                                bot.deleteMessage(chat_id, update.message.message_id)
                            except:
                                pass
                    else:
                        if proceed:
                            bot.sendMessage(chat_id, s, disable_web_page_preview=True, parse_mode="HTML")
                if update.message['text'].startswith("/settag") and isenabled("settag"):
                    if chat_type == "channel":
                        if update.message['text'] == "/settag":
                            f = open("tags.txt","w+")
                            s = f.read().split("\n")
                            for line in s:
                                if not str(chat_id) in line:
                                    f.write(line)
                            f.close()
                        else:
                            try:
                                input_text = update.message['text'].split("/settag @")[1]
                            except:
                                try:
                                    input_text = update.message['text'].split("/settag ")[1]
                                except:
                                    pass
                            f = open("tags.txt","a")
                            f.write(str(chat_id) + ":" + input_text + "\n")
                            f.close()
                update.messageid = None
                try:
                    input_text = update.message['text']
                    input_text = input_text.split('&')[0]
                    if "group" in chat_type and "/conv" in input_text:
                        goon = True
                        input_text = input_text.replace("/conv", "").replace(" ", "")
                    else:
                        if "group" in chat_type:
                            goon = False
                        else:
                            goon = True
                    blacklist = open("blacklist.txt", "r").read()
                    if str(chat_id) in blacklist:
                        goon = False
                        done = True
                    if "album" in input_text or "list" in update.message['text'] or "set" and "soundcloud" in input_text:
                        goon = False
                        done = True
                        if chat_type == "private":
                            bot.sendMessage(chat_id, "I cannot convert multiple songs at once, sorry...")
                    if goon == True and done == False:
                        if not chat_type == "channel" and not "group" in chat_type and not input_text.startswith("/") and "http" in update.message["text"] and "://" in update.message["text"] and not input_text.startswith("#"):
                            status_message = bot.sendMessage(chat_id, "Downloading...")
                        else:
                            try:
                                if input_text.startswith("/") or "youtu" in input_text \
                                or "mixcloud" in input_text \
                                or "soundcloud" in input_text \
                                or "spotify" in input_text:
                                    bot.deleteMessage(telepot.message_identifier(update.message))
                            except:
                                pass
                        # Apparently some users are so dumb, that they forgot what an URL is
                        # Thanks StackOverflow: https://stackoverflow.com/questions/839994/extracting-a-url-in-python
                        try:
                            input_text = input_text.replace("\n", " ")
                            input_text = re.search("(?P<url>https?://[^\s]+)", input_text).group("url") # pylint: disable=W1401
                        except:
                            pass
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
                            cmd = ["youtube-dl", "--add-metadata", "-x", "--no-continue", "--prefer-ffmpeg", "--extract-audio", "--write-thumbnail", "--embed-thumbnail", "-v", "--audio-format", "mp3", "--output", "audio.%%(ext)s", input_text]
                            subprocess.Popen(cmd, shell=False).wait()
                            r = requests.get(input_text)
                            c = r.content
                            title = c.split('<title>')[1].split('</title>')[0]
                            stitle = html.unescape(title.split(' by ')[0])
                            artist = html.unescape(title.split(' by ')[1].split(' | Mixcloud')[0].split(',')[0])
                            title = stitle
                            filename = artist.replace(" ", "-").replace("/", "-") + "_" + title.replace(" ", "-").replace("/", "-") + ".mp3"
                            cover = "https://thumbnailer.mixcloud.com/unsafe/800x800/extaudio/" + c.split('src="https://thumbnailer.mixcloud.com/unsafe/60x60/extaudio/')[1].split('"')[0]
                            os.system("wget -O audio.jpg \"" + cover + "\"")
                            if not chat_type == "channel" and not "group" in chat_type:
                                bot.editMessageText(update.messageid, "Converting...")
                            subprocess.Popen(["lame", "--tc", "@" + bottag, "-b", "320", "--ti", "audio.jpg", "--ta", artist, "--tt", title, "audio.mp3", filename], shell=False).wait()
                            audio = MP3(filename)
                            length = audio.info.length * 0.33
                            l2 = (audio.info.length * 0.33) + 60
                            if audio.info.length > l2:
                                subprocess.Popen(str("ffmpeg -ss " + str(length) + " -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                            else:
                                subprocess.Popen(str("ffmpeg -ss 0 -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                            if not chat_type == "channel" and not "group" in chat_type:
                                bot.editMessageText(update.messageid, "Sending...")
                            f = open("audio.jpg")
                            bot.sendPhoto(chat_id,"audio.jpg","🎵 " + title + "\n🎤 " + artist + username)
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
                                bot.sendMessage(chat_id,"Here you go!\nCheck out @kseverythingbot_army for news and informations about this bot.",disable_web_page_preview=True)
                        if "spotify" in input_text:
                            try:
                                trackid = input_text.replace("https://open.spotify.com/track/", "").split("?")[0]
                            except:
                                trackid = input_text.replace("https://open.spotify.com/track/", "")
                            print(trackid)
                            with urllib.request.urlopen(input_text) as response:
                                r = response.read().decode()
                            title = r.split('<title>')[1].split('</title>')[0]
                            stitle = html.unescape(title.split(',')[0])
                            artist = html.unescape(title.split(', a song by ')[1].split(' on Spotify')[0].split(',')[0])
                            if " (feat." in stitle:
                                stitle = stitle.split(' (')[0]
                            title = stitle
                            data = r.split('Spotify.Entity = ')[1].split(';')[0]
                            cover = data.split('"url":"')[1].split("\"")[0].replace("\\", "")
                            year = data.split('"release_date":"')[1].split('"')[0].split('-')[0]
                            albumtitle = data.split('"name":"')[2].split('"')[0].split('-')[0]
                            os.system("wget -O audio.jpg \"" + cover + "\"")
                            query = artist.replace("(", " ").replace(")", "").lower() + " " + title.replace("(", " ").replace(")", "").lower().replace(" ", "+")
                            print(query)
                            cmd = ["youtube-dl", "--no-continue", "--add-metadata", "-x", "--prefer-ffmpeg", "--extract-audio", "-v", "--audio-format", "mp3", "--output", "audio.%%(ext)\"", "ytsearch:\"" + query + "\""]
                            subprocess.Popen(cmd, shell=False).wait()
                            filename = artist.replace(" ", "-").replace("/", "-") + "_" + title.replace(" ", "-").replace("/", "-") + ".mp3"
                            if not chat_type == "channel" and not "group" in chat_type:
                                bot.editMessageText(text="Converting...", message_id=status_message.message_id, chat_id=chat_id)
                            subprocess.Popen(["lame", "-b", "320", "--tc", "@" + bottag, "--ti", "audio.jpg", "--ta", artist, "--tt", title, "--ty", year, "--tl", albumtitle, "audio.mp3", filename], shell=False).wait()
                            audio = MP3(filename)
                            length = audio.info.length * 0.33
                            l2 = (audio.info.length * 0.33) + 60
                            if audio.info.length > l2:
                                subprocess.Popen(str("ffmpeg -ss " + str(length) + " -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                            else:
                                subprocess.Popen(str("ffmpeg -ss 0 -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                            if not chat_type == "channel" and not "group" in chat_type:
                                bot.editMessageText(text="Sending...", message_id=status_message.message_id, chat_id=chat_id)
                            f = open("audio.jpg")
                            sendPhoto(chat_id,"audio.jpg","🎵 " + title + "\n🎤 " + artist + "\n💿 " + albumtitle + "\n📆 " + year + username)
                            f.close()
                            if os.path.exists("audio.jpg"):
                                os.system("convert audio.jpg -resize 90x90 thumb.jpg")
                            else:
                                os.system("convert blank.jpg -resize 90x90 thumb.jpg")
                            sendAudioChan(chat_id,filename,artist,title,username,thumb)
                            sendVoice(chat_id,"output.ogg",username)
                            if chat_type == "private":
                                bot.sendMessage(chat_id,"Here you go!\nCheck out @kseverythingbot_army for news and informations about this bot.",disable_web_page_preview=True)
                        if "soundcloud" in input_text:
                            track = client.get('/resolve', url=input_text)
                            thist = track
                            filename = thist.title.replace(" ", "_").replace("!", "_").replace("&", "_").replace("?", "_") + ".mp3"
                            stream_url = client.get(thist.stream_url, allow_redirects=False)
                            artist = None
                            title = None
                            try:
                                artist = thist.title.split(" - ")[0]
                                title = thist.title.split(" - ")[1]
                                try:
                                    artist = artist.split(" [")[0]
                                    title = title.split(" [")[0]
                                except:
                                    pass
                                try:
                                    os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                                    os.system("wget \"" + track.artwork_url.replace("-large", "-crop") + "?t500x500\" -O raw_audio.jpg")
                                except:
                                    pass
                                if not os.path.exists("raw_audio.jpg"):
                                    os.system("wget \"" + track.user['avatar_url'].replace("-large", "-t500x500") + "\" -O raw_audio.jpg")
                                    os.system("convert raw_audio.jpg -resize 800x800 audio.jpg")
                                os.system("rm -f raw_audio.jpg")
                                if not chat_type == "channel" and not "group" in chat_type:
                                    bot.editMessageText(update.messageid, "Converting...")
                                subprocess.Popen(["lame", "--tc", "@" + bottag, "-b", "320", "--ti", "audio.jpg", "--ta", artist, "--tt", title, "audio.mp3", filename], shell=False).wait()
                            except:
                                artist = thist.user['username']
                                title = thist.title
                                try:
                                    artist = artist.split(" [")[0]
                                    title = title.split(" [")[0]
                                except:
                                    pass
                                try:
                                    os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                                    os.system("wget \"" + track.artwork_url.replace("-large", "-crop") + "?t500x500\" -O raw_audio.jpg")
                                except:
                                    pass
                                if not os.path.exists("raw_audio.jpg"):
                                    os.system("wget \"" + track.user['avatar_url'].replace("-large", "-t500x500") + "\" -O raw_audio.jpg")
                                    os.system("convert raw_audio.jpg -resize 800x800 audio.jpg")
                                os.system("rm -f raw_audio.jpg")
                                if not chat_type == "channel" and not "group" in chat_type:
                                    bot.editMessageText(update.messageid, "Converting...")
                                try:
                                    subprocess.Popen(["lame", "-b", "320", "--tc", "@" + bottag, "--ti", "audio.jpg", "--ta", artist, "--tt", title, "audio.mp3", filename], shell=False).wait()
                                except:
                                    subprocess.Popen(["lame", "-b", "320", "--tc", "@" + bottag, "--ta", artist, "--tt", title, "audio.mp3", filename], shell=False).wait()
                            audio = MP3(filename)
                            length = audio.info.length * 0.33
                            l2 = (audio.info.length * 0.33) + 60
                            if audio.info.length > l2:
                                subprocess.Popen(str("ffmpeg -ss " + str(length) + " -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                            else:
                                subprocess.Popen(str("ffmpeg -ss 0 -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                            if not chat_type == "channel" and not "group" in chat_type:
                                bot.editMessageText(update.messageid, "Sending...")
                            f = open("audio.jpg")
                            bot.sendPhoto(chat_id,"audio.jpg","🎵 " + title + "\n🎤 " + artist + username)
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
                                bot.sendMessage(chat_id,"Here you go!\nCheck out @kseverythingbot_army for news and informations about this bot.",disable_web_page_preview=True)
                        if "youtu" in input_text:
                            input_text = input_text.replace("music.", "")
                            cmd = ["youtube-dl", "--add-metadata", "-x", "--no-continue", "--prefer-ffmpeg", "--extract-audio", "--write-thumbnail", "--embed-thumbnail", "-v", "--audio-format", "mp3", "--output", "audio.%%(ext)s", input_text]
                            subprocess.Popen(cmd, shell=False).wait()
                            tag = eyed3.load("audio.mp3")
                            try:
                                title = tag.tag.title.split(" - ")[1].replace("\"", "")
                                artist = tag.tag.title.split(" - ")[0]
                                title = title.replace(artist + " - ","")
                                try:
                                    if not "Remix" in title and not "Mix" in title:
                                        title = title.split(" (")[0].replace("\"", "")
                                except:
                                    pass
                                try:
                                    title = title.split(" [")[0].replace("\"", "")
                                except:
                                    pass
                            except:
                                title = tag.tag.title.replace("\"", "")
                                artist = tag.tag.artist
                            try:
                                artist = artist.replace(" - Topic", "")
                            except:
                                pass
                            try:
                                subprocess.Popen(["sacad", artist, title, "800", "audio.jpg"], shell=False).wait()
                            except:
                                pass
                            if not chat_type == "channel" and not "group" in chat_type:
                                bot.editMessageText(text="Converting...", message_id=status_message.message_id, chat_id=chat_id)
                            filename = filename = artist.replace(" ", "-").replace("/", "-") + "_" + title.replace(" ", "-").replace("/", "-") + ".mp3"
                            subprocess.Popen(["lame", "--tc", "@" + bottag, "-b", "320", "--ti", "audio.jpg", "--ta", artist, "--tt", title, "audio.mp3", filename], shell=False).wait()
                            audio = MP3(filename)
                            length = audio.info.length * 0.33
                            l2 = (audio.info.length * 0.33) + 60
                            if audio.info.length > l2:
                                subprocess.Popen(str("ffmpeg -ss " + str(length) + " -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                            else:
                                subprocess.Popen(str("ffmpeg -ss 0 -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                            if not chat_type == "channel" and not "group" in chat_type:
                                bot.editMessageText(text="Sending...", message_id=status_message.message_id, chat_id=chat_id)
                            f = open("audio.jpg")
                            sendPhoto(chat_id,"audio.jpg","🎵 " + title + "\n🎤 " + artist + username)
                            f.close()
                            if os.path.exists("audio.jpg"):
                                os.system("convert audio.jpg -resize 90x90 thumb.jpg")
                            else:
                                os.system("convert blank.jpg -resize 90x90 thumb.jpg")
                            sendAudioChan(chat_id,filename,artist,title,username,thumb)
                            sendVoice(chat_id,"output.ogg",username)
                            f.close()
                            if chat_type == "private":
                                bot.sendMessage(chat_id,"Here you go!\nCheck out @kseverythingbot_army for news and informations about this bot.",disable_web_page_preview=True)
                        try:
                            bot.deleteMessage(chat_id, status_message.message_id)
                        except:
                            pass
                except Exception as e:
                    if chat_type == "private":
                        f = open("templates/error", "r")
                        s = f.read()
                        f.close()
                        exc_type, exc_obj, tb = sys.exc_info()
                        print(exc_type, exc_obj, tb)
                        f = tb.tb_frame
                        lineno = tb.tb_lineno
                        error = str("line " + str(lineno) + ": " + str(e))
                        url = update.message["text"]
                        chatid = str(chat_id)
                        release = str(subprocess.check_output("git rev-parse --verify HEAD", shell=True)).replace("b'", "").replace("'", "").replace("\\n", "")
                        s = s.replace("%%crashlog%%", error)
                        s = s.replace("%%message%%", url)
                        s = s.replace("%%chatid%%", chatid)
                        s = s.replace("%%release%%", release)
                        s = s.replace("%%bottag%%", bottag)
                        try:
                            bot.deleteMessage(update.messageid)
                            bot.sendMessage(chat_id, "<pre>An error occured. It has been reported to my owner.</pre>", parse_mode="HTML")
                        except:
                            bot.sendMessage(chat_id, "<pre>An error occured. It has been reported to my owner.</pre>", parse_mode="HTML")
                        try:
                            f = open("chatids.txt")
                            c = f.readlines()
                            f.close()
                            master = ""
                            for x in c:
                                if BOTMASTER in x:
                                    master = x.split(":")[0]
                            bot.sendMessage(master, s, parse_mode="HTML")
                        except:
                            pass
                else:
                    f = open("counters-disabled.txt", "r")
                    s = f.read()
                    f.close()
                    if not chat_type == "channel" and not chat_type == "private" and isenabled("counters") and not str(chat_id) in s:
                        if "😂" in update.message['text']:
                            count = len(update.message['text'].split("😂")) - 1
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
                        if "bro" in update.message['text']:
                            count = len(update.message['text'].split("bro")) - 1
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
                        if "Hi" in update.message['text']:
                            count = len(update.message['text'].split("Hi")) - 1
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
                        if "lol" in update.message['text']:
                            count = len(update.message['text'].split("lol")) - 1
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
                        if "pp" in update.message['text']:
                            count = len(update.message['text'].split("pp")) - 1
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
                    if update.message['text'].startswith("/ping") and isenabled("ping"):
                        ping = os.popen("ping -c1 www.google.com").read().split("time=")[1].split(" ms")[0]
                        bot.sendMessage(chat_id, "Pong! (" + ping + " ms)")
                    if update.message['text'].startswith("/start") and chat_type == "private":
                        f = open("templates/start")
                        s = f.read()
                        f.close()
                        bot.sendMessage(chat_id,s)
                    if update.message['text'].startswith("/addextra") and isenabled("extras"):
                        try:
                            extraname = update.message['text'].replace('/addextra ', '').replace(':', '').replace('#', '').split('\n')[0]
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
                                    f.write(str(telepot.message_identifier(update.message['reply_to_message'])) + ":" + extraname + ":" + str(chat_id) + "\n")
                                    f.close()
                                    f = open("extras/" + str(chat_id) + "-extralist.txt", "a")
                                    f.write(extraname + "\r\n")
                                    f.close()
                                    bot.sendMessage(chat_id, "Extra added!")
                                else:
                                    bot.sendMessage(chat_id, "Extra already exists!")
                            else:
                                admins = bot.getChatAdministrators(chat_id)
                                isAdmin = False
                                for user in admins:
                                    try:
                                        if str(user['user']['username']).replace("u'", "").replace("'", "") == update.message.from_user.username:
                                            isAdmin = True
                                    except:
                                        pass
                                if update.message.from_user.username == BOTMASTER:
                                    isAdmin = True
                                if isAdmin == True:
                                    if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                        extraname = update.message['text'].split('/addextra ')[1].replace(':', '').replace('#', '').split('\n')[0]
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
                                            f.write(str(telepot.message_identifier(update.message['reply_to_message'])) + ":" + extraname + ":" + str(chat_id) + "\n")
                                            f.close()
                                            f = open("extras/" + str(chat_id) + "-extralist.txt", "a")
                                            f.write(extraname + "\r\n")
                                            f.close()
                                            bot.sendMessage(chat_id, "Extra added!")
                                        else:
                                            bot.sendMessage(chat_id, "Extra already exists!")
                                    else:
                                        bot.sendMessage(chat_id, "Error: Permission denied while trying to add extra!")
                                else:
                                    bot.sendMessage(chat_id, "Error: Permission denied while trying to add extra!")
                        except:
                            bot.sendMessage(chat_id, "Message not a reply to a message or no name defined! Reply to a message with /addextra [name]")
                    if update.message['text'].startswith('#') or update.message['text'].startswith("/extra ") and isenabled("extras"):
                        try:
                            if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                if update.message['text'].startswith("/extra "):
                                    extraname = update.message['text'].split('/extra ')[1].replace('#', '').split('\n')[0]
                                else:
                                    extraname = update.message['text'].split('#')[1].split('\n')[0]
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
                                    update.message = bot.forwardMessage(chat_id, chat_id, int(mid))
                                except:
                                    bot.sendMessage(chat_id, "Error: Extra not found!")
                                try:
                                    # Some stuff is pretty tricky here. You shouldn't change the order here if this function isn't broken.
                                    if "document" in str(update.message):
                                        fileid = update.message.document.file_id
                                        bot.sendDocument(chat_id, fileid)
                                    if "sticker" in str(update.message):
                                        fileid = update.message.sticker.file_id
                                        bot.sendSticker(chat_id, fileid)
                                    if "voice" in str(update.message):
                                        fileid = update.message.voice.file_id
                                        bot.sendVoice(chat_id, fileid)
                                    if "video_note" in str(update.message):
                                        fileid = update.message.video_note.file_id
                                        bot.sendVideoNote(chat_id, fileid)
                                    if "video" in str(update.message):
                                        fileid = update.message.video.file_id
                                        bot.sendVideo(chat_id, fileid)
                                    if "photo" in str(update.message):
                                        fileid = update.message.photo.file_id
                                        bot.sendPhoto(chat_id, fileid)
                                    if "audio" in str(update.message):
                                        fileid = update.message.audio.file_id
                                        bot.sendAudio(chat_id, fileid)
                                    if "file" in str(update.message):
                                        fileid = update.message.document.file_id
                                        bot.sendDocument(chat_id, fileid)
                                    if "text" in str(update.message):
                                        bot.sendMessage(chat_id, update.message['text'])
                                except:
                                    pass
                                try:
                                    bot.deleteMessage(telepot.message_identifier(update.message))
                                except:
                                    pass
                        except:
                            bot.sendMessage(chat_id, "Error: Extra not found!")
                    if update.message['text'].startswith("/extralist") or update.message['text'].startswith("/extras") and isenabled("extras"):
                        try:
                            if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                f = open("extras/" + str(chat_id) + "-extralist.txt", "r")
                                bot.sendDocument(chat_id, f)
                                f.close()
                        except:
                            bot.sendMessage(chat_id, "Error: No extras available!")
                    if update.message['text'].startswith("/delextra") and isenabled("extras"):
                        if " " in update.message['text']:
                            extraname = update.message['text'].split('/delextra ')[1].replace('#', '').split('\n')[0]
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
                                for user in admins:
                                    try:
                                        if str(user['user']['username']).replace("u'", "").replace("'", "") == update.message.from_user.username:
                                            isAdmin = True
                                    except:
                                        pass
                                if update.message.from_user.username == BOTMASTER:
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
                    if not chat_type == "private" and update.message["text"].startswith("/disableextras") and isenabled("extras"):
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == update.message.from_user.username:
                                    isAdmin = True
                            except:
                                pass
                        if update.message.from_user.username == BOTMASTER:
                            isAdmin = True
                        if isAdmin == True:
                            os.system("touch extras/" + str(chat_id) + "-deactivated.txt")
                            bot.sendMessage(chat_id, "Success: Extras disabled!")
                    if not chat_type == "private" and update.message["text"].startswith("/enableextras") and isenabled("extras"):
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == update.message.from_user.username:
                                    isAdmin = True
                            except:
                                pass
                        if update.message.from_user.username == BOTMASTER:
                            isAdmin = True
                        if isAdmin == True:
                            os.system("rm -f extras/" + str(chat_id) + "-deactivated.txt")
                            bot.sendMessage(chat_id, "Extras enabled!")
                    if not chat_type == "private" and update.message['text'].startswith("/disablecounters") and isenabled("counters"):
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == update.message.from_user.username:
                                    isAdmin = True
                            except:
                                pass
                        if update.message.from_user.username == BOTMASTER:
                            isAdmin = True
                        if isAdmin == True:
                            f = open("counters-disabled.txt", "a+")
                            f.write(str(chat_id) + "\n")
                            f.close()
                            bot.sendMessage(chat_id, "Success: Counters disabled")
                    if not chat_type == "private" and update.message['text'].startswith("/enablecounters") and isenabled("counters"):
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == update.message.from_user.username:
                                    isAdmin = True
                            except:
                                pass
                        if update.message.from_user.username == BOTMASTER:
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

def sendVoice(chat_id,file_name,text):
    url = "https://api.telegram.org/bot%s/sendVoice"%(TOKEN)
    files = {'voice': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'caption' : text}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendPhoto(chat_id,file_name,caption):
    url = "https://api.telegram.org/bot%s/sendPhoto"%(TOKEN)
    files = {'photo': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'caption': caption}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

print('Listening ...')

def main():
    global update_id
    bot = telegram.Bot(TOKEN)
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            handle(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            update_id += 1

if __name__ == '__main__':
    main()