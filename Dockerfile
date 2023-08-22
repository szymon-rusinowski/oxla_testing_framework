FROM ubuntu:20.04 AS development
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update;\
    apt-get install -y python3-pip postgresql

#COPY ./requirements.txt /usr/src/app/
#RUN pip3 install -r /usr/src/app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#FROM development as release

#COPY ./src /src
#COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

