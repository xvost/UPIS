FROM ubuntu:latest

LABEL proxy=0.3

RUN apt update && apt upgrade -y && apt-get clean

RUN apt update && apt install ca-certificates python3 python3-dev python3-pip -y && apt-get clean

WORKDIR /app

COPY ./ /app

RUN pip3 install -r ./requirements.txt

ENTRYPOINT ["./start_install.py"]

CMD ["-h"]