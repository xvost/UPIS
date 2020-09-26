FROM ubuntu:latest

LABEL proxy '0.1'

RUN apt update && apt upgrade -y && apt-get clean

RUN apt update && apt install openssl curl gnupg2 lsb-release ca-certificates python3 uwsgi uwsgi-plugin-python3 gcc python3-dev musl-dev python3-pip -y

RUN pip3 install django requests configobj

RUN echo "deb http://nginx.org/packages/mainline/ubuntu `lsb_release -cs` nginx" | tee /etc/apt/sources.list.d/nginx.list && \
curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add -

RUN apt update && apt install nginx

COPY ./config/upis_nginx.conf /etc/nginx/conf.d/default.conf
COPY ./config/upis_uwsgi.conf /etc/uwsgi/apps-enabled/upis.conf

WORKDIR /app

COPY ./ /app

ENTRYPOINT nginx -g 'daemon off;' & uwsgi --ini /etc/uwsgi/apps-enabled/upis.conf --plugins python3