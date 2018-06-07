FROM  debian:latest

WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y git curl python python-pip python3 python3-pip lame ffmpeg libchromaprint-dev libchromaprint-tools libchromaprint1 wget imagemagick
RUN curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
RUN chmod a+rx /usr/local/bin/youtube-dl
RUN pip2 install -r requirements2.txt
RUN pip3 install -r requirements3.txt
CMD ["python2", "main.py"]
