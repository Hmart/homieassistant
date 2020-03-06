FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir -p /mnt/logs/

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    git && \
    rm -rf /var/lib/apt/lists/*

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt pyuwsgi

RUN apt-get --purge autoremove -y \
    build-essential \
    python3-dev

ADD uwsgi.ini /etc/uwsgi/app.ini

ADD ./homieassistant /app

EXPOSE 3030 8000

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/app.ini"]
