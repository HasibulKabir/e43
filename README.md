# Everything downloader Bot

This Telegram bot can download almost anything :)

[koyu.space](http://koyu.space)

## Installation

### Requirements

- NodeJS (latest version)
- FFMPEG
- LAME
- eyeD3
- node-acoustid
- chromaprint
- Python 2
- Python 3
- youtube-dl
- wget
- Sacad

### How to install

```
git clone https://github.com/koyuawsmbrtn/everythingbot
cd everythingbot
npm install git+https://github.com/AllToMP3/alltomp3
sudo npm -g install acoustid
sudo pip2 install -r requirements2.txt
sudo pip3 install -r requirements3.txt
```

Fill in your bot token into the `TOKEN` variable in the file `main.py` and then run it with `python2 main.py`

Done! :)

#### Docker instructions

```
sudo docker build .
sudo docker images
```

Find the recent built image name and run it with `sudo docker run [YOUR-IMAGE]`

You can remove old images with `sudo docker rmi -f [YOUR-IMAGE]`

**License: DBAD Public License**