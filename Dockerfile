FROM python:3.9-alpine


ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
#install mysqlclient but better with mysql conecctor Django instead using mysql-connector-python
#RUN apk add --update --no-cache
#RUN apk add --update --no-cache --virtual .tmp-build-deps \
#      gcc python3-dev musl-dev mariadb-dev

#RUN apk update \
#    && apk add --virtual build-deps gcc python3-dev musl-dev \
#    && apk add --no-cache mariadb-dev

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps


RUN pip install -r /requirements.txt
#RUN pip install mysqlclient

#RUN apk del .tmp-build-deps
#RUN apk del build-deps


# Setup directory structure
RUN mkdir /ecomerceflow
WORKDIR /ecomerceflow
COPY ./ecomerceflow/ /ecomerceflow

RUN adduser -D user
USER user