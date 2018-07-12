FROM debian:latest

WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get -y dist-upgrade
RUN apt-get -y install wget zlib1g-dev build-essential libssl-dev openssl libreadline-dev ffmpeg aria2
RUN cd ~ && wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz && tar zxf Python-3.6.1.tgz && cd ~/Python-3.6.1 && ./configure && make -j4 && make install
RUN pip3.6 install -r requirements.txt
CMD ["python3.6", "main.py"]
