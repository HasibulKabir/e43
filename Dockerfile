FROM alpine:latest

WORKDIR /app
ADD . /app

RUN echo http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
RUN apk update
RUN apk upgrade
RUN apk add git curl python py-pip python3 lame ffmpeg build-base python-dev python3-dev py-pip jpeg-dev zlib-dev py-lxml libmagic
RUN python3 -m ensurepip
RUN pip2 install --upgrade pip
RUN pip3 install --upgrade pip
RUN pip2 install -r requirements2.txt
RUN pip3 install -r requirements3.txt
CMD ["python2", "main.py"]