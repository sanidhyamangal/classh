FROM python:3.8.6-slim-buster

LABEL Name=classh Version=0.0.1
EXPOSE 8000

WORKDIR /app
ADD . /app

## Install libmysql-dev
 RUN apt-get clean && \
        apt-get update && \
        apt-get install -y \
        build-essential \
        default-libmysqlclient-dev

# # Using pip:
RUN python -m pip install -r requirements.txt
