

## Requirements

Python 3.7.0+

## Usage

Install required packages

```
apt update && apt -y install sshpass git python3-virtualenv
```

Clone repo
```
git clone https://github.com/xvost/UPIS.git
```

Create and prepare virtual env

```
cd ./UPIS/
virtualenv venv
source ./venv/bin/activate
pip3 install -r ./requirements.txt
```

### Use config mode
Change dir

Rename data.conf
```
cp ./data.conf.example ./data_ipv6.conf
```
or
```
cp ./data.conf.example ./data_ipv4.conf
```
Edit data.conf
```
editor ./data_ipv6.conf
```
Start script
```
./start_install.py -n ipv6 -c
```

### Or use interactive mode
Change dir
```
cd ./UPIS
```
Start script at interactive mode
```
./start_install.py -n ipv6 -i
```
### Help

```
./start_install.py -h
```
## Known problems

1. Only Debian 8 with 3.* kernel at proxies nodes
2. Do not permit install ipv6 and ipv4 together.

## May use as docker container

Need installed [docker engine](https://docs.docker.com/engine/install/)

Use script `./install_as_command.sh` to build and setup command

Usage: `upis -h`
