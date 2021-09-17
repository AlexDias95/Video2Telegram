FROM python:3

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y build-essential \
    curl \
    libssl-dev \
    libffi-dev \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /tmp/*
RUN pip install --upgrade setuptools \
    python-telegram-bot \
    requests \
    inotify \
    nose \
    ffmpy

ADD file2gif.py /

CMD [ "python", "/file2gif.py" ]
