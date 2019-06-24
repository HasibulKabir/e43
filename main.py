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
import soundcloud
import string
import json
import urllib.request
import html.parser
import logging
import telegram
import requests
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
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
    MODULES = 'spotify,youtube,soundcloud,mixcloud,voice,videonotes,help,commands,stats,extras,counters,ud,subscriptions,videos,boxxy,horny,settag,ping,kick,ban,delete,pin,promote'
f = open("random.txt", "w+")
f.write(str(random.randint(10,30)))
f.close()

VERSION = "0.9.0"

def isenabled(chat_id, module):
    blacklist = open("blacklist.txt", "r").read()
    modenabled = False
    for x in MODULES.split(','):
        if x == module:
            modenabled = True
    if str(chat_id) in blacklist:
        modenabled = False
    if "*" in blacklist:
        modenabled = False
    return modenabled

def getduration(dlcmd):
    dlcmd = "youtube-dl -j " + dlcmd
    if "youtube.com" in dlcmd or "youtu.be" in dlcmd:
        args = dlcmd.split(" ")
        args2 = ["jq", ".duration"]
        process_dl = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
        process_jq = subprocess.Popen(args2, stdin=process_dl.stdout, stdout=subprocess.PIPE, shell=False)
        process_dl.stdout.close()
        try:
            return int(str(process_jq.communicate()[0]).replace("b'", "").replace("\\n'", ""))
        except:
            return None
    else:
        return 0

def handle(bot):
    blacklist = open("blacklist.txt", "r").read()
    if not "*" in blacklist:
        global update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1
            if update.effective_message:
                os.system("sh clean.sh")
                try:
                    botlang = update.effective_message.from_user.language_code
                    if "de" in botlang:
                        botlang = "de"
                    else:
                        botlang = "c"
                except:
                    botlang = "c"
                done = False
                bottag = bot.getMe()["username"]
                f = open("random.txt", "r")
                rnumber = int(f.read())
                f.close()
                chat_type = update.effective_message.chat.type
                chat_id = update.effective_message.chat_id
                isAdmin = False
                try:
                    admins = bot.getChatAdministrators(chat_id)
                    for user in admins:
                        try:
                            if str(user['user']['username']).replace("u'", "").replace("'", "") == bottag:
                                isAdmin = True
                        except:
                            pass
                except:
                    pass
                def start():
                    f = open("lang/" + botlang + "/start")
                    s = f.read()
                    f.close()
                    if bottag == "e43bot":
                        s = s.replace("%%name%%", "E43")
                    else:
                        if botlang == "de":
                            s = s.replace("%%name%%", bot.getMe().first_name + ", ein Klon von E43")
                        else:
                            s = s.replace("%%name%%", bot.getMe().first_name + ", a clone of E43")
                    try:
                        fileid = bot.getUserProfilePhotos(bot.getMe().id).photos[0][0].file_id
                        bot.sendPhoto(chat_id,fileid,s)
                    except:
                        os.system("convert e43.png -resize 512x512 thumb.jpg")
                        bot.sendPhoto(chat_id,open("thumb.jpg", "rb"),s)
                        os.system("rm -f thumb.jpg")
                if not isAdmin and "group" in chat_type:
                    if os.path.exists("deadlines/" + str(chat_id) + "-admin.txt"):
                        f = open("deadlines/" + str(chat_id) + "-admin.txt", "r")
                        s = f.read()
                        f.close()
                        if int(time.time()) > int(s.split(".")[0]):
                            bot.leaveChat(chat_id)
                            try:
                                os.system("rm -f deadlines/" + str(chat_id) + "-admin.txt")
                            except:
                                pass
                    else:
                        ts3 = str(time.time() + 180)
                        f = open("deadlines/" + str(chat_id) + "-admin.txt", "w+")
                        f.write(ts3)
                        f.close()
                        start()
                        f = open("lang/" + botlang + "/deadline", "r")
                        s = f.read()
                        f.close()
                        bot.sendMessage(chat_id, s)
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
                                f.write(str(chat_id) + ":" + update.effective_message.from_user.username + "\n")
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
                if update.effective_message.audio and isenabled(chat_id, "voice"):
                    try:
                        fileid = update.effective_message.audio.file_id
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
                        sendVoice(update.effective_message.chat_id, "output.ogg","")
                    except:
                        pass
                if update.effective_message.video and isenabled(chat_id, "videonotes"):
                    try:
                        fileid = update.effective_message.video.file_id
                        print(fileid)
                        print(bot.getFile(file_id=fileid))
                        filename = bot.getFile(file_id=fileid)['file_path']
                        os.system("wget https://api.telegram.org/file/bot" + TOKEN + "/" + filename + " -O " + filename)
                        os.system("ffmpeg -ss 0 -t 59 -y -i " + filename + " -strict -2 -c:v libx264 -crf 26 -vf scale=480:480 vm.mp4")
                        sendVideoNote(chat_id, "vm.mp4")
                    except:
                        pass
                if update.effective_message.text:
                    if "group" in chat_type:
                        if update.effective_message["text"].startswith("/kick") or update.effective_message["text"].startswith("/ban") or update.effective_message["text"].startswith("/delete") or update.effective_message["text"].startswith("/promote"):
                            admins = bot.getChatAdministrators(chat_id)
                            isAdmin = False
                            proceed = False
                            for user in admins:
                                try:
                                    if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                        isAdmin = True
                                except:
                                    pass
                            if update.effective_message.from_user.username == BOTMASTER:
                                isAdmin = True
                            if isAdmin == True:
                                proceed = True
                            else:
                                bot.sendMessage(chat_id, "You don't have permission to do that.", reply_to_message_id=update.effective_message.message_id)
                            if proceed:
                                if update.effective_message["text"].startswith("/kick") or update.effective_message["text"].startswith("/ban"):
                                    try:
                                        if isenabled(chat_id, "ban"):
                                            userid = update.effective_message.reply_to_message.from_user.id
                                            bot.kickChatMember(chat_id, userid)
                                        if update.effective_message["text"].startswith("/kick") and isenabled(chat_id, "kick"):
                                            userid = update.effective_message.reply_to_message.from_user.id
                                            bot.kickChatMember(chat_id, userid)
                                            bot.unbanChatMember(chat_id, userid)
                                    except:
                                        pass
                                if update.effective_message["text"].startswith("/promote") and isenabled(chat_id, "promote"):
                                    try:
                                        if isenabled(chat_id, "promote"):
                                            userid = update.effective_message.reply_to_message.from_user.id
                                            bot.promoteChatMember(chat_id, userid)
                                    except:
                                        pass
                                if update.effective_message["text"].startswith("/pin") and isenabled(chat_id, "pin"):
                                    try:
                                        if isenabled(chat_id, "pin"):
                                            msgid = update.effective_message.message_id
                                            bot.pinChatMessage(chat_id, msgid)
                                    except:
                                        pass
                                if update.effective_message["text"].startswith("/delete") or update.effective_message["text"].startswith("/del"):
                                    if isenabled(chat_id, "delete"):
                                        try:
                                            bot.deleteMessage(chat_id, update.effective_message.reply_to_message.message_id)
                                            bot.deleteMessage(chat_id, update.effective_message.message_id)
                                        except:
                                            try:
                                                bot.deleteMessage(chat_id, update.effective_message.message_id)
                                            except:
                                                pass
                    if update.effective_message["text"].startswith("/ud") and isenabled(chat_id, "ud"):
                        try:
                            if "group" in chat_type:
                                if update.effective_message.text == "/ud" or update.effective_message.text == "/ud@" + bottag:
                                    input_text = update.effective_message.reply_to_message.text
                                else:
                                    input_text = update.effective_message.text
                            else:
                                input_text = update.effective_message.text
                            try:
                                input_text = input_text.split(" ")[len(input_text.split(" ")) - 1]
                            except:
                                pass
                            word = str(input_text.replace("/ud ", "").replace("/ud@" + bottag + " ", ""))
                            with urllib.request.urlopen("https://api.urbandictionary.com/v0/define?term=" + word) as response:
                                r = response.read().decode()
                            callback = json.loads(r)
                            definition = callback["list"][0]["definition"]
                            bot.sendMessage(chat_id, "Definition for <b>" + callback["list"][0]["word"].capitalize() + "</b>:\n\n" + definition, parse_mode="HTML", reply_to_message_id=update.effective_message.message_id)
                        except:
                            bot.sendMessage(chat_id, "Can't find definition!", reply_to_message_id=update.effective_message.message_id)
                    if update.effective_message["text"].startswith("/stats") and isenabled(chat_id, "stats"):
                        f = open("lang/" + botlang + "/stats")
                        s = f.read()
                        f.close()
                        err_nope = "not applicable"
                        err_disabled = "disabled"
                        err_unset = "not set"
                        s = s.replace("%%chat_id%%", str(chat_id))
                        if chat_type == "channel":
                            f = open("tags.txt","r")
                            t = f.read().split("\n")
                            f.close()
                            username = ""
                            for line in t:
                                chanid = line.split(":")[0]
                                if chanid == str(chat_id):
                                    username = line.split(":")[1]
                            if not username == "":
                                s = s.replace("%%channel_id%%", username)
                            else:
                                s = s.replace("%%channel_id%%", err_unset)
                        else:
                            if isenabled(chat_id, "settag"):
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
                            if isenabled(chat_id, "subscriptions"):
                                s = s.replace("%%subscribed%%", err_nope)
                            else:
                                s = s.replace("%%subscribed%%", err_disabled)
                        if "group" in chat_type:
                            f = open("counters-disabled.txt")
                            x = f.read()
                            f.close()
                            if isenabled(chat_id, "counters"):
                                if str(chat_id) in x:
                                    s = s.replace("%%counters%%", "deactivated")
                                else:
                                    s = s.replace("%%counters%%", "activated")
                            else:
                                s = s.replace("%%counters%%", err_disabled)
                        else:
                            if isenabled(chat_id, "counters"):
                                s = s.replace("%%counters%%", err_nope)
                            else:
                                s = s.replace("%%counters%%", err_disabled)
                        if "group" in chat_type or chat_type == "channel":
                            if isenabled(chat_id, "extras"):
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
                        bot.sendMessage(chat_id, s, parse_mode="HTML", reply_to_message_id=update.effective_message.message_id)
                    if update.effective_message["text"].startswith("/unsub") and isenabled(chat_id, "subscriptions"):
                        if ALLOWUNSUBS == 'TRUE':
                            if chat_type == "private" or "group" in chat_type:
                                proceed = False
                                if "group" in chat_type:
                                    admins = bot.getChatAdministrators(chat_id)
                                    isAdmin = False
                                    for user in admins:
                                        try:
                                            if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                                isAdmin = True
                                        except:
                                            pass
                                    if update.effective_message.from_user.username == BOTMASTER:
                                        isAdmin = True
                                    if isAdmin == True:
                                        proceed = True
                                    else:
                                        bot.sendMessage(chat_id, "You don't have permission to do that.", reply_to_message_id=update.effective_message.message_id)
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
                                    bot.sendMessage(chat_id, "Success: Unsubscribed!", reply_to_message_id=update.effective_message.message_id)
                        else:
                            bot.sendMessage(chat_id, "My bot owner doesn't allow me to unsubscribe :(", reply_to_message_id=update.effective_message.message_id)
                    if update.effective_message["text"].startswith("/sub") and isenabled(chat_id, "subscriptions"):
                        if chat_type == "private" or "group" in chat_type:
                            proceed = False
                            if "group" in chat_type:
                                admins = bot.getChatAdministrators(chat_id)
                                isAdmin = False
                                for user in admins:
                                    try:
                                        if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                            isAdmin = True
                                    except:
                                        pass
                                if update.effective_message.from_user.username == BOTMASTER:
                                    isAdmin = True
                                if isAdmin == True:
                                    proceed = True
                                else:
                                    bot.sendMessage(chat_id, "You don't have permission to do that.", reply_to_message_id=update.effective_message.message_id)
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
                                    f.write(str(chat_id) + ":" + update.effective_message["from"]["username"] + "\n")
                                    f.close()
                                except:
                                    if chat_type == "private":
                                        f = open("chatids.txt", "a+")
                                    else:
                                        f = open("chatids2.txt", "a+")
                                    f.write(str(chat_id) + "\n")
                                    f.close()
                                bot.sendMessage(chat_id, "Success: Subscribed!", reply_to_message_id=update.effective_message.message_id)
                    if update.effective_message['text'].startswith("/boxxy") and isenabled(chat_id, "boxxy"):
                        sendVoice(chat_id, "assets/boxxy.ogg","")
                    if update.effective_message['text'].startswith("/horny") and isenabled(chat_id, "horny"):
                        sendVoice(chat_id, "assets/horny.ogg","")
                    if update.effective_message['text'].startswith("/vid http://") or update.effective_message['text'].startswith("/vid https://"):
                        if isenabled(chat_id, "videos"):
                            try:
                                input_text = update.effective_message['text'].split("/vid ")[1]
                                input_text = input_text.split('&')[0]
                                duration = getduration(input_text)
                                if duration>1000:
                                    f = open("lang/" + botlang + "/toolong", "r")
                                    s = f.read()
                                    f.close()
                                    bot.sendMessage(chat_id,s,disable_web_page_preview=True,reply_to_message_id=update.effective_message.message_id)
                                    done = True
                                else:
                                    status_message = bot.sendMessage(chat_id, "Downloading...", reply_to_message_id=update.effective_message.message_id)
                                    cmd_download = ["youtube-dl", "--no-continue", "-f", "mp4", "-o", "video.%(ext)s", input_text]
                                    subprocess.Popen(cmd_download, shell=False).wait()
                                    cmd_conv = "ffmpeg -y -i video.mp4 -vcodec libx264 -crf 27 -preset veryfast -c:a copy -s 640x360 out.mp4"
                                    if not chat_type == "channel" and not "group" in chat_type:
                                        bot.editMessageText(text="Converting...", message_id=status_message.message_id, chat_id=chat_id)
                                    subprocess.Popen(cmd_conv.split(' '), shell=False).wait()
                                    filename = "out.mp4"
                                    subprocess.Popen(str("ffmpeg -ss 0 -t 59 -y -i " + filename + " -vcodec libx264 -crf 27 -preset veryfast -c:a copy -s 480x480 vm.mp4").split(' '), shell=False).wait()
                                    if not chat_type == "channel" and not "group" in chat_type:
                                        bot.editMessageText(text="Sending...", message_id=status_message.message_id, chat_id=chat_id)
                                    try:
                                        sendVideoNote(chat_id, "vm.mp4")
                                        sendVideo(chat_id, "out.mp4")
                                        if chat_type == "private":
                                            bot.sendMessage(chat_id,"Here you go!\nCheck out @kseverythingbot_army for news and informations about this bot.",disable_web_page_preview=True)
                                    except:
                                        goon = False
                                        done = True
                                        f = open("lang/" + botlang + "/unavailable", "r")
                                        s = f.read()
                                        f.close()
                                        bot.sendMessage(chat_id,s,disable_web_page_preview=True,reply_to_message_id=update.effective_message.message_id)
                            except Exception as e:
                                if chat_type == "private":
                                    f = open("lang/" + botlang + "/error", "r")
                                    s = f.read()
                                    f.close()
                                    exc_type, exc_obj, tb = sys.exc_info()
                                    print(exc_type, exc_obj, tb)
                                    f = tb.tb_frame
                                    lineno = tb.tb_lineno
                                    error = str("line " + str(lineno) + ": " + str(e))
                                    url = update.effective_message["text"]
                                    chatid = str(chat_id)
                                    release = str(subprocess.check_output("git rev-parse --verify HEAD", shell=True)).replace("b'", "").replace("'", "").replace("\\n", "")
                                    s = s.replace("%%crashlog%%", error)
                                    s = s.replace("%%message%%", url)
                                    s = s.replace("%%chatid%%", chatid)
                                    s = s.replace("%%release%%", release)
                                    s = s.replace("%%bottag%%", bottag)
                                    try:
                                        bot.deleteMessage(chat_id, update.effective_message.message_id)
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
                    try:
                        if update.effective_message['text'].startswith("/help") or update.effective_message['text'].startswith("/commands"):
                            if update.effective_message['text'].startswith("/commands" ) and isenabled(chat_id, "commands"):
                                f = open("lang/" + botlang + "/commands", "r")
                                s = f.read()
                                f.close()
                                commands = ""
                                for mods in MODULES.split(","):
                                    try:
                                        if isenabled(chat_id, mods):
                                            f = open("lang/" + botlang + "/cmdplates/" + mods, "r")
                                            command = f.read()
                                            f.close()
                                            commands = commands + command + "\n"
                                    except:
                                        pass
                                s = s.replace("%%commands%%", commands)
                            if update.effective_message['text'].startswith("/help") and isenabled(chat_id, "help"):
                                f = open("lang/" + botlang + "/help", "r")
                                s = f.read()
                                f.close()
                                release = str(subprocess.check_output("git rev-parse --verify HEAD", shell=True)).replace("b'", "").replace("'", "").replace("\\n", "")
                                s = s.replace("%%bottag%%", "@" + bottag).replace("%%botmaster%%", "@" + BOTMASTER).replace("%%release%%", release).replace("%%version%%", VERSION)
                            if "group" in chat_type:
                                f = open("chatids.txt", "r")
                                cids = f.read()
                                f.close()
                                f = open("subsoff.txt", "r")
                                cids = cids + f.read()
                                f.close()
                                try:
                                    if update.effective_message.from_user.username in cids:
                                        try:
                                            for x in cids.split("\n"):
                                                if x.split(":")[1] == update.effective_message.from_user.username:
                                                    cid = int(x.split(":")[0])
                                        except:
                                            pass
                                        bot.sendMessage(cid, s, disable_web_page_preview=True, parse_mode="HTML")
                                        try:
                                            bot.deleteMessage(chat_id, update.effective_message.message_id)
                                        except:
                                            pass
                                    else:
                                        bot.sendMessage(chat_id, "There was a problem sending you the help. Press the link below, send me any message and try again to receive the help.\nhttps://t.me/" + bottag, reply_to_message_id=update.effective_message.message_id)
                                except:
                                    try:
                                        bot.sendMessage(chat_id, "There was a problem sending you the help. Press the link below and start me to receive the help.\nhttps://t.me/" + bottag, reply_to_message_id=update.effective_message.message_id)
                                    except:
                                        pass
                            else:
                                bot.sendMessage(chat_id, s, disable_web_page_preview=True, parse_mode="HTML", reply_to_message_id=update.effective_message.message_id)
                    except:
                        pass
                    if update.effective_message['text'].startswith("/settag") and isenabled(chat_id, "settag"):
                        if chat_type == "channel":
                            if update.effective_message['text'] == "/settag":
                                f = open("tags.txt","w+")
                                s = f.read().split("\n")
                                for line in s:
                                    if not str(chat_id) in line:
                                        f.write(line)
                                f.close()
                            else:
                                try:
                                    input_text = update.effective_message['text'].split("/settag @")[1]
                                except:
                                    try:
                                        input_text = update.effective_message['text'].split("/settag ")[1]
                                    except:
                                        pass
                                f = open("tags.txt","a")
                                f.write(str(chat_id) + ":" + input_text + "\n")
                                f.close()
                    update.effective_messageid = None
                    if done == False:
                        try:
                            input_text = update.effective_message['text']
                            input_text = input_text.split('&')[0]
                            if "group" in chat_type and "/conv" in input_text:
                                goon = True
                                input_text = input_text.replace("/conv", "").replace(" ", "")
                            else:
                                if "group" in chat_type:
                                    goon = False
                                else:
                                    goon = True
                            try:
                                if update.effective_message.reply_to_message.text == "/conv" or "/conv@" + bottag and "group" in chat_type:
                                    input_text = update.effective_message.reply_to_message.text.replace("/conv", "")
                            except:
                                pass
                            blacklist = open("blacklist.txt", "r").read()
                            if str(chat_id) in blacklist:
                                goon = False
                                done = True
                            if "album" in input_text or "list" in update.effective_message['text'] or "set" in input_text:
                                goon = False
                                done = True
                                if chat_type == "private":
                                    bot.sendMessage(chat_id, "I cannot convert multiple songs at once, sorry...", reply_to_message_id=update.effective_message.message_id)
                            duration = getduration(input_text)
                            if chat_type == "channel":
                                goon = True
                                done = False
                            try:
                                if duration>1000:
                                        goon = False
                                        done = True
                                        f = open("lang/" + botlang + "/toolong", "r")
                                        s = f.read()
                                        f.close()
                                        bot.sendMessage(chat_id,s,disable_web_page_preview=True,reply_to_message_id=update.effective_message.message_id)
                            except:
                                goon = False
                                done = True
                                f = open("lang/" + botlang + "/unavailable", "r")
                                s = f.read()
                                f.close()
                                bot.sendMessage(chat_id,s,disable_web_page_preview=True,reply_to_message_id=update.effective_message.message_id)
                            if goon == True and done == False:
                                if not chat_type == "channel" and not "group" in chat_type and not input_text.startswith("/") and "http" in update.effective_message["text"] and "://" in update.effective_message["text"] and not input_text.startswith("#"):
                                    status_message = bot.sendMessage(chat_id, "Downloading...", reply_to_message_id=update.effective_message.message_id)
                                else:
                                    try:
                                        if input_text.startswith("/settag") or "youtu" in input_text \
                                        or "mixcloud" in input_text \
                                        or "soundcloud" in input_text \
                                        or "spotify" in input_text:
                                            bot.deleteMessage(chat_id, update.effective_message.message_id)
                                    except:
                                        pass
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
                                    cover = "https://thumbnailer.mixcloud.com/unsafe/500x500/extaudio/" + c.split('src="https://thumbnailer.mixcloud.com/unsafe/60x60/extaudio/')[1].split('"')[0]
                                    os.system("wget -O audio.jpg \"" + cover + "\"")
                                    if not chat_type == "channel" and not "group" in chat_type:
                                        bot.editMessageText(update.effective_messageid, "Converting...")
                                    subprocess.Popen(["lame", "--tc", "@" + bottag, "-b", "320", "--ti", "audio.jpg", "--ta", artist, "--tt", title, "audio.mp3", filename], shell=False).wait()
                                    audio = MP3(filename)
                                    length = audio.info.length * 0.33
                                    l2 = (audio.info.length * 0.33) + 60
                                    if audio.info.length > l2:
                                        subprocess.Popen(str("ffmpeg -ss " + str(length) + " -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                                    else:
                                        subprocess.Popen(str("ffmpeg -ss 0 -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg").split(' '), shell=False).wait()
                                    if not chat_type == "channel" and not "group" in chat_type:
                                        bot.editMessageText(update.effective_messageid, "Sending...")
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
                                    stitle = html.unescape(title.split(', a song by ')[0])
                                    artist = html.unescape(title.split(', a song by ')[1].split(' on Spotify')[0])
                                    if " (feat." in stitle:
                                        stitle = stitle.split(' (')[0]
                                    title = stitle
                                    data = r.split('Spotify.Entity = ')[1].split(';')[0]
                                    cover = data.split('"url":"')[1].split("\"")[0].replace("\\", "")
                                    year = data.split('"release_date":"')[1].split('"')[0].split('-')[0]
                                    albumtitle = data.split('"name":"')[2].split('"')[0].split('-')[0]
                                    os.system("wget -O audio.jpg \"" + cover + "\"")
                                    query = artist.replace("(", " ").replace(")", "").lower() + " " + title.replace("(", " ").replace(")", "").lower().replace(" ", "+") + "+official+audio"
                                    print(query)
                                    cmd = ["youtube-dl", "--no-continue", "--add-metadata", "-x", "--prefer-ffmpeg", "--extract-audio", "-v", "--audio-format", "mp3", "--output", "audio.%%(ext)\"", "ytsearch:\"" + query + "\""]
                                    subprocess.Popen(cmd, shell=False).wait()
                                    filename = artist.replace(" ", "-").replace("/", "-") + "_" + title.replace(" ", "-").replace("/", "-") + ".mp3"
                                    if not chat_type == "channel" and not "group" in chat_type:
                                        bot.editMessageText(text="Converting...", message_id=status_message.message_id, chat_id=chat_id)
                                    subprocess.Popen(["lame", "-b", "320", "--tc", "@" + bottag, "--ti", "audio.jpg", "--ta", artist, "--tt", title, "--ty", year, "--tl", albumtitle, "audio.mp3", filename], shell=False).wait()
                                    try:
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
                                    except:
                                        goon = False
                                        done = True
                                        f = open("lang/" + botlang + "/unavailable", "r")
                                        s = f.read()
                                        f.close()
                                        bot.sendMessage(chat_id,s,disable_web_page_preview=True,reply_to_message_id=update.effective_message.message_id)
                                if "soundcloud" in input_text:
                                    track = client.get('/resolve', url=input_text)
                                    thist = track
                                    filename = thist.title.replace(" ", "_").replace("!", "_").replace("&", "_").replace("?", "_").replace("/", "-") + ".mp3"
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
                                        if not chat_type == "channel" and not "group" in chat_type:
                                            bot.editMessageText(text="Converting...", message_id=status_message.message_id, chat_id=chat_id)
                                        subprocess.Popen(["lame", "--tc", "@" + bottag, "-b", "320", "--ti", "raw_audio.jpg", "--ta", artist, "--tt", title, "audio.mp3", filename], shell=False).wait()
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
                                        if not chat_type == "channel" and not "group" in chat_type:
                                            bot.editMessageText(text="Converting...", message_id=status_message.message_id, chat_id=chat_id)
                                        try:
                                            subprocess.Popen(["lame", "-b", "320", "--tc", "@" + bottag, "--ti", "raw_audio.jpg", "--ta", artist, "--tt", title, "audio.mp3", filename], shell=False).wait()
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
                                        bot.editMessageText(text="Sending...", message_id=status_message.message_id, chat_id=chat_id)
                                    sendPhoto(chat_id,"raw_audio.jpg","🎵 " + title + "\n🎤 " + artist + username)
                                    if os.path.exists("audio.jpg"):
                                        os.system("convert audio.jpg -resize 90x90 thumb.jpg")
                                    else:
                                        os.system("convert blank.jpg -resize 90x90 thumb.jpg")
                                    sendAudioChan(chat_id,filename,artist,title,username,thumb)
                                    f = open("output.ogg", "rb")
                                    bot.sendVoice(chat_id,f,"",username)
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
                                        subprocess.Popen(["sacad", artist, title, "500", "audio.jpg"], shell=False).wait()
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
                        except Exception as e:
                            if chat_type == "private":
                                f = open("lang/" + botlang + "/error", "r")
                                s = f.read()
                                f.close()
                                exc_type, exc_obj, tb = sys.exc_info()
                                print(exc_type, exc_obj, tb)
                                f = tb.tb_frame
                                lineno = tb.tb_lineno
                                error = str("line " + str(lineno) + ": " + str(e))
                                url = update.effective_message["text"]
                                chatid = str(chat_id)
                                release = str(subprocess.check_output("git rev-parse --verify HEAD", shell=True)).replace("b'", "").replace("'", "").replace("\\n", "")
                                s = s.replace("%%crashlog%%", error)
                                s = s.replace("%%message%%", url)
                                s = s.replace("%%chatid%%", chatid)
                                s = s.replace("%%release%%", release)
                                s = s.replace("%%bottag%%", bottag)
                                try:
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
                    f = open("counters-disabled.txt", "r")
                    s = f.read()
                    f.close()
                    if not chat_type == "channel" and not chat_type == "private" and isenabled(chat_id, "counters") and not str(chat_id) in s:
                        if "😂" in update.effective_message['text']:
                            count = len(update.effective_message['text'].split("😂")) - 1
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
                        if "bro" in update.effective_message['text']:
                            count = len(update.effective_message['text'].split("bro")) - 1
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
                        if "Hi" in update.effective_message['text']:
                            count = len(update.effective_message['text'].split("Hi")) - 1
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
                        if "lol" in update.effective_message['text']:
                            count = len(update.effective_message['text'].split("lol")) - 1
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
                        if "pp" in update.effective_message['text']:
                            count = len(update.effective_message['text'].split("pp")) - 1
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
                    if update.effective_message['text'].startswith("/ping") and isenabled(chat_id, "ping"):
                        ping = os.popen("ping -c1 www.google.com").read().split("time=")[1].split(" ms")[0]
                        bot.sendMessage(chat_id, "Pong! (" + ping + " ms)", reply_to_message_id=update.effective_message.message_id)
                    if update.effective_message['text'].startswith("/start") and chat_type == "private":
                        start()
                    if update.effective_message['text'].startswith("/addextra") and isenabled(chat_id, "extras"):
                        try:
                            extraname = update.effective_message['text'].replace('/addextra ', '').replace(':', '').replace('#', '').split('\n')[0]
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
                                    print(update.effective_message["reply_to_message"].message_id)
                                    f.write(str(update.effective_message.reply_to_message.message_id) + ":" + extraname + ":" + str(chat_id) + "\n")
                                    f.close()
                                    f = open("extras/" + str(chat_id) + "-extralist.txt", "a")
                                    f.write(extraname + "\r\n")
                                    f.close()
                                    bot.sendMessage(chat_id, "Extra added!", reply_to_message_id=update.effective_message.message_id)
                                else:
                                    bot.sendMessage(chat_id, "Extra already exists!", reply_to_message_id=update.effective_message.message_id)
                            else:
                                admins = bot.getChatAdministrators(chat_id)
                                isAdmin = False
                                for user in admins:
                                    try:
                                        if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                            isAdmin = True
                                    except:
                                        pass
                                if update.effective_message.from_user.username == BOTMASTER:
                                    isAdmin = True
                                if isAdmin == True:
                                    if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                        extraname = update.effective_message['text'].split('/addextra ')[1].replace(':', '').replace('#', '').split('\n')[0]
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
                                            f.write(str(telepot.message_identifier(update.effective_message['reply_to_message'])) + ":" + extraname + ":" + str(chat_id) + "\n")
                                            f.close()
                                            f = open("extras/" + str(chat_id) + "-extralist.txt", "a")
                                            f.write(extraname + "\r\n")
                                            f.close()
                                            bot.sendMessage(chat_id, "Extra added!", reply_to_message_id=update.effective_message.message_id)
                                        else:
                                            bot.sendMessage(chat_id, "Extra already exists!", reply_to_message_id=update.effective_message.message_id)
                                    else:
                                        bot.sendMessage(chat_id, "Error: Permission denied while trying to add extra!", reply_to_message_id=update.effective_message.message_id)
                                else:
                                    bot.sendMessage(chat_id, "Error: Permission denied while trying to add extra!", reply_to_message_id=update.effective_message.message_id)
                        except:
                            bot.sendMessage(chat_id, "Message not a reply to a message or no name defined! Reply to a message with /addextra [name]", reply_to_message_id=update.effective_message.message_id)
                    if update.effective_message['text'].startswith('#') or update.effective_message['text'].startswith("/extra "):
                        if isenabled(chat_id, "extras"):
                            try:
                                if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                    if update.effective_message['text'].startswith("/extra "):
                                        extraname = update.effective_message['text'].split('/extra ')[1].replace('#', '').split('\n')[0]
                                    else:
                                        extraname = update.effective_message['text'].split('#')[1].split('\n')[0]
                                    f = open("extras/" + str(chat_id) + ".txt", "r")
                                    s = f.read().split('\n')
                                    f.close()
                                    mid = None
                                    for x in s:
                                        if not x == "":
                                            ename = x.split(':')[1]
                                            if ename == extraname:
                                                mid = x.split(':')[0]
                                                cid = x.split(':')[2]
                                    try:
                                        status_message = bot.forwardMessage(chat_id, chat_id, int(mid))
                                    except:
                                        bot.sendMessage(chat_id, "Error: Extra not found!", reply_to_message_id=update.effective_message.message_id)
                                    try:
                                        if "document" in str(status_message):
                                            fileid = status_message.document.file_id
                                            bot.sendDocument(chat_id, fileid, reply_to_message_id=update.effective_message.message_id)
                                        if "sticker" in str(status_message):
                                            fileid = status_message.sticker.file_id
                                            bot.sendSticker(chat_id, fileid, reply_to_message_id=update.effective_message.message_id)
                                        if "voice" in str(status_message):
                                            fileid = status_message.voice.file_id
                                            bot.sendVoice(chat_id, fileid, reply_to_message_id=update.effective_message.message_id)
                                        if "video_note" in str(status_message):
                                            fileid = status_message.video_note.file_id
                                            bot.sendVideoNote(chat_id, fileid, reply_to_message_id=update.effective_message.message_id)
                                        if "video" in str(status_message):
                                            fileid = status_message.video.file_id
                                            bot.sendVideo(chat_id, fileid, reply_to_message_id=update.effective_message.message_id)
                                        if "photo" in str(status_message):
                                            fileid = status_message.photo.file_id
                                            bot.sendPhoto(chat_id, fileid, reply_to_message_id=update.effective_message.message_id)
                                        if "audio" in str(status_message):
                                            fileid = status_message.audio.file_id
                                            bot.sendAudio(chat_id, fileid, reply_to_message_id=update.effective_message.message_id)
                                        if "file" in str(status_message):
                                            fileid = status_message.document.file_id
                                            bot.sendDocument(chat_id, fileid, reply_to_message_id=update.effective_message.message_id)
                                        if "text" in str(status_message):
                                            bot.sendMessage(chat_id, status_message['text'], reply_to_message_id=update.effective_message.message_id)
                                    except:
                                        pass
                            except:
                                pass
                    if update.effective_message['text'].startswith("/extralist") or update.effective_message['text'].startswith("/extras") and isenabled(chat_id, "extras"):
                        try:
                            if not os.path.isfile("extras/" + str(chat_id) + "-deactivated.txt"):
                                f = open("extras/" + str(chat_id) + "-extralist.txt", "r")
                                bot.sendDocument(chat_id, f, reply_to_message_id=update.effective_message.message_id)
                                f.close()
                        except:
                            bot.sendMessage(chat_id, "Error: No extras available!", reply_to_message_id=update.effective_message.message_id)
                    if update.effective_message['text'].startswith("/extradel") and isenabled(chat_id, "extras"):
                        if " " in update.effective_message['text']:
                            extraname = update.effective_message['text'].split('/extradel ')[1].replace('#', '').split('\n')[0]
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
                                try:
                                    for line in linesb:
                                        if not line == extraname+"\r\n":
                                            f.write(line)
                                    f.close()
                                    actuallyDidIt = True
                                except:
                                    pass
                                if actuallyDidIt == True:
                                    bot.sendMessage(chat_id, "Success: Extra deleted!", reply_to_message_id=update.effective_message.message_id)
                                else:
                                    bot.sendMessage(chat_id, "Error: Extra doesn't exist.", reply_to_message_id=update.effective_message.message_id)
                            if not chat_type == "private":
                                admins = bot.getChatAdministrators(chat_id)
                                isAdmin = False
                                for user in admins:
                                    try:
                                        if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                            isAdmin = True
                                    except:
                                        pass
                                if update.effective_message.from_user.username == BOTMASTER:
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
                                            bot.sendMessage(chat_id, "Success: Extra deleted!", reply_to_message_id=update.effective_message.message_id)
                                        else:
                                            bot.sendMessage(chat_id, "Error: Extra doesn't exist.", reply_to_message_id=update.effective_message.message_id)
                                    else:
                                        bot.sendMessage(chat_id, "Error: Permission denied while trying to delete extra!", reply_to_message_id=update.effective_message.message_id)
                                else:
                                    bot.sendMessage(chat_id, "Error: Permission denied while trying to delete extra!", reply_to_message_id=update.effective_message.message_id)
                        else:
                            bot.sendMessage(chat_id, "Error: Missing parameter!", reply_to_message_id=update.effective_message.message_id)
                    if not chat_type == "private" and update.effective_message["text"].startswith("/disableextras") and isenabled(chat_id, "extras"):
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                    isAdmin = True
                            except:
                                pass
                        if update.effective_message.from_user.username == BOTMASTER:
                            isAdmin = True
                        if isAdmin == True:
                            os.system("touch extras/" + str(chat_id) + "-deactivated.txt")
                            bot.sendMessage(chat_id, "Success: Extras disabled!", reply_to_message_id=update.effective_message.message_id)
                    if not chat_type == "private" and update.effective_message["text"].startswith("/enableextras") and isenabled(chat_id, "extras"):
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                    isAdmin = True
                            except:
                                pass
                        if update.effective_message.from_user.username == BOTMASTER:
                            isAdmin = True
                        if isAdmin == True:
                            os.system("rm -f extras/" + str(chat_id) + "-deactivated.txt")
                            bot.sendMessage(chat_id, "Extras enabled!", reply_to_message_id=update.effective_message.message_id)
                    if not chat_type == "private" and update.effective_message['text'].startswith("/disablecounters") and isenabled(chat_id, "counters"):
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                    isAdmin = True
                            except:
                                pass
                        if update.effective_message.from_user.username == BOTMASTER:
                            isAdmin = True
                        if isAdmin == True:
                            f = open("counters-disabled.txt", "a+")
                            f.write(str(chat_id) + "\n")
                            f.close()
                            bot.sendMessage(chat_id, "Success: Counters disabled", reply_to_message_id=update.effective_message.message_id)
                    if not chat_type == "private" and update.effective_message['text'].startswith("/enablecounters") and isenabled(chat_id, "counters"):
                        admins = bot.getChatAdministrators(chat_id)
                        isAdmin = False
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == update.effective_message.from_user.username:
                                    isAdmin = True
                            except:
                                pass
                        if update.effective_message.from_user.username == BOTMASTER:
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
                            bot.sendMessage(chat_id, "Success: Counters enabled!", reply_to_message_id=update.effective_message.message_id)
                except:
                    pass
                try:
                    bot.deleteMessage(chat_id, status_message.message_id)
                except:
                    pass

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

def sendVideo(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendVideo"%(TOKEN)
    files = {'video': open(file_name, 'rb')}
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
