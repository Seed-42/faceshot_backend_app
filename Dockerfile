#FROM python:3.6.9-slim-stretch
FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
RUN apt-get update && apt-get install -y pkg-config \
                                        build-essential \
                                        python3-pip \
                                        python3-dev \
                                        python3-distutils \
                                        python3-pkg-resources \
                                        python3-tk \
                                        git
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN mkdir -p /app/logs && touch /app/logs/app_log.log
WORKDIR /app
RUN mkdir -p /app/tmp
COPY src/ .

ENV APP_HOST 0.0.0.0
ENV APP_PORT 7000
ENV APP_LOG_PATH /app/logs
ENV APP_LOG_LEVEL DEBUG
ENV APP_TEMP_PATH /app/tmp

# CMD exec gunicorn --bind :$APP_PORT --workers 1 --threads 8 --timeout 0 main:app
CMD ["gunicorn","--bind","0.0.0.0:7000","main","--timeout=300"]