#!/bin/bash
wget -q -P /tmp \
  https://bitbucket.org/pypy/pypy/downloads/pypy3-v5.10.1-linux64.tar.bz2 
sudo tar -x -C /opt -f /tmp/pypy3-v5.10.1-linux64.tar.bz2
rm /tmp/pypy3-v5.10.1-linux64.tar.bz2
sudo mv /opt/pypy3-v5.10.1-linux64 /opt/pypy3
sudo ln -s /opt/pypy3/bin/pypy3 /usr/local/bin/pypy3