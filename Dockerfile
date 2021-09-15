FROM ubuntu:bionic

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y python build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /tmp/*
RUN pip3 install --upgrade setuptools \
    python-telegram-bot \
    inotify \
    requests \
    ffmpy

ADD file2gif.py /

CMD [ "python", "./file2gif.py" ]
