import sys
import asyncio
import telepot
import os
import subprocess
import requests
import html
import soundcloud
import pylast
import urllib.parse
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

TOKEN = os.environ["TOKEN"]

# Initializing APIs
client = soundcloud.Client(client_id='LBCcHmRB8XSStWL6wKH2HPACspQlXg2P')
API_KEY = "9d3ee2a574eb3bb2a6f0a4e108e46ceb"
API_SECRET = "f982de3bd2d8e7ffe5c117b568b1fc3e"
lastfm = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

# Initalizing Telegram API functions

def sendAudio(chat_id,file_name,performer,title):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'performer' : performer, 'title' : title}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendVideoNote(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendVideoNote"%(TOKEN)
    files = {'video_note': open(file_name, 'rb')}
    data = {'chat_id' : chat_id}
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

class EverythingBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(EverythingBot, self).__init__(*args, **kwargs)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        bottag = (await bot.getMe())["username"]
        if content_type == 'audio':
            audiofile = msg['audio']
            fileid = msg['audio']['file_id']
            flavor = telepot.flavor(msg)
            summary = telepot.glance(msg, flavor=flavor)
            print(flavor, summary)
            print(fileid)
            if not os.path.exists("output" + str(fileid) + ".ogg"):
                filename = (await bot.getFile(file_id=fileid))['file_path']
                os.system(str("aria2c -x16 https://api.telegram.org/file/bot" + TOKEN + "/" + filename + " -o " + filename + " --allow-overwrite=\"false\" --auto-file-renaming=\"false\""))
                if ".mp3" in filename:
                    audio = MP3(filename)
                    length = str(audio.info.length * 0.33)
                    l2 = (audio.info.length * 0.33) + 60
                if ".m4a" in filename:
                    audio = MP4(filename)
                    length = str(audio.info.length * 0.33)
                    l2 = (audio.info.length * 0.33) + 60
                if audio.info.length > l2:
                    os.system(str("ffmpeg -ss " + length + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output" + str(fileid) + ".ogg"))
                else:
                    os.system(str("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output" + str(fileid) + ".ogg"))
            sendVoice(chat_id, "output" + str(fileid) + ".ogg")
        if content_type == "text":
            if msg["text"].startswith("/ping"):
                ping = os.popen("ping -c1 www.google.com").read().split("time=")[1].split(" ms")[0]
                await self.sender.sendMessage("Pong! (" + ping + " ms)")
            if msg["text"].startswith("/debug "):
                cmd = msg["text"].split("/debug ")[1]
                if cmd == "bottag":
                    await self.sender.sendMessage(bottag)
            if msg["text"].startswith("http://") or msg["text"].startswith("https://"):
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
                msgid = None
                if chat_type == "private":
                    message = (await self.sender.sendMessage("Downloading..."))
                    msgid = telepot.message_identifier(message)
                try:
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
                        os.system("lame -b 320 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                        audio = MP3("audio.mp3")
                        length = audio.info.length * 0.33
                        l2 = length + 60
                        if audio.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                        f = open("audio.jpg")
                        await self.sender.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist + username)
                        f.close()
                        if chat_type == "channel":
                            sendAudioChan(chat_id,"audio.mp3",artist,title,username)
                        else:
                            sendAudio(chat_id,"audio.mp3",artist,title)
                        f = open("output.ogg", "r")
                        await self.sender.sendVoice(chat_id,f,username)
                        f.close()
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
                        query = urllib.parse.quote(artist + " - " + title)
                        print(query)
                        cmd = "youtube-dl --geo-bypass --add-metadata -x --prefer-ffmpeg --extract-audio -v --audio-format mp3 --output \"audio.%%(ext)\" \"gvsearch1:" + query + "\""
                        subprocess.check_call(cmd, shell=True)
                        filename = artist.replace(" ", "-").replace("/", "-") + "_" + title.replace(" ", "-").replace("/", "-") + ".mp3"
                        os.system("lame -b 320 --ti audio.jpg  --ty " + year + " --tl \"" + albumtitle + "\" --tc @" + bottag + " --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                        audio = MP3(filename)
                        length = audio.info.length * 0.33
                        l2 = (audio.info.length * 0.33) + 60
                        if audio.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                        f = open("audio.jpg")
                        bot.sendPhoto(chat_id,f,"🎵 " + title + "\n🎤 " + artist + username)
                        f.close()
                        sendAudioChan(chat_id,filename,artist,title,username)
                        f = open("output.ogg", "r")
                        bot.sendVoice(chat_id,f,username)
                        f.close()
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
                            os.system("lame -b 320 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
                        except:
                            printable = set(string.printable)
                            artist = filter(lambda x: x in printable, thist.user['username'])
                            printable = set(string.printable)
                            title = filter(lambda x: x in printable, thist.title)
                            os.system("wget \"" + stream_url.location + "\" -O audio.mp3")
                            os.system("wget \"" + track.artwork_url.replace("-large", "-crop") + "?t500x500\" -O raw_audio.jpg")
                            os.system("convert raw_audio.jpg -resize 800x800 audio.jpg")
                            os.system("rm -f raw_audio.jpg")
                            os.system("lame -b 320 --ti audio.jpg --ta \"" + artist + "\" --tt \"" + title + "\" audio.mp3 \"" + filename + "\"")
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
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                        f = open("output.ogg", "r")
                        bot.sendVoice(chat_id,f,username)
                        f.close()
                    if "youtu" in input_text:
                        input_text = input_text.replace("music.", "")
                        cmd = 'youtube-dl --geo-bypass --add-metadata -x --prefer-ffmpeg --extract-audio -v --audio-format mp3 \
                            --output audio.%%(ext)s %summary'%(input_text)
                        subprocess.check_call(cmd.split(), shell=False)
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
                        subprocess.Popen(["sacad", artist, title, "800", "audio.jpg"], shell=False).wait()
                        artist = artist.replace(" - Topic", "")
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
                        try:
                            sendAudioChan(chat_id,filename,artist,title,username)
                        except:
                            filename = "audio.mp3"
                            sendAudioChan(chat_id,filename,artist,title,username)
                        audio = eyed3.load("audio.mp3")
                        tt = audio.tag.title
                        artist = audio.tag.artist
                        ad = MP3("audio.mp3")
                        length = ad.info.length * 0.33
                        l2 = length + 60
                        if ad.info.length > l2:
                            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"audio.mp3\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                        else:
                            os.system("ffmpeg -ss 0 -t 60 -y -i \"audio.mp3\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
                        f = open("output.ogg", "r")
                        bot.sendVoice(chat_id,f,username)
                        f.close()
                except Exception as e:
                    f = open("errormsg.txt", "r")
                    s = f.read()
                    f.close()
                    error = str(e)
                    message = msg["text"]
                    chatid = str(chat_id)
                    release = subprocess.check_output("git rev-parse --verify HEAD", shell=True)
                    s = s.replace("%crashlog%", error).relace("%message%", message).replace("%chatid%", chatid).replace("release", release)
                    await self.sender.sendMessage(chat_id, s)

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, EverythingBot, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()
