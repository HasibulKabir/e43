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

Build your own image with (if you changed the source code)

```
sudo docker build .
sudo docker images
```

and find the recent built image name with `sudo docker images` and run it with `sudo docker run -d -t -i -e TOKEN='[YOUR-TOKEN]' [YOUR-IMAGE]` (you can remember the command line arguments with a mnemonic like "DeTie" or "Daemon Tie")

You can remove old images with `sudo docker rmi -f [YOUR-IMAGE]`

You can also list currently running containers with `sudo docker container ls` and stop them with ``sudo docker stop [CONTAINER] && sudo docker rm -f [CONTAINER]`

The official image can be found at `koyuawsmbrtn/everythingbot` on Docker Hub. It's recommended if you haven't modified the source-code, because it's already pre-built. (I would recommend to modify the source-code to your needs anyway)

**License: DBAD Public License**