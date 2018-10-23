FROM  archlinux/base:latest

WORKDIR /app
ADD . /app

RUN pacman -Syyuu --noconfirm
RUN pacman -S base-devel chromaprint wget curl ffmpeg lame python2 python2-pip python python-pip imagemagick youtube-dl --noconfirm
RUN pip2 install -r requirements2.txt
RUN pip3 install -r requirements3.txt
CMD ["python2", "main.py"]