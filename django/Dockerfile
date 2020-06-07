FROM ubuntu:20.04

WORKDIR /app
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt install -y -q --no-install-recommends \
                      ffmpeg \
                      dnsutils \
                      libmysqlclient-dev \
                      mysql-common \
                      gcc \
                      libglib2.0-0 \
                      libsm6 \
                      libxext6 \
                      libxrender-dev \
                      python3-mysqldb \
                      python3-pymysql \
                      python3-pip && \
    apt-get clean && \
    rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*
ADD requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

ADD . .

EXPOSE 8080
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile","/log/gu.log ", "video_archive.wsgi"]
