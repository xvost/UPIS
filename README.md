

## Requirements

Ansible 2.7.0+

Python 3.6.0+

## Usage

Clone repo
```
git clone https://github.com/xvost/Ansible_proxies.git
```
Change dir
```
cd ./Ansible_proxies
```
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
./start_install.py -c ipv6
```

OR

Change dir
```
cd ./Ansible_proxies
```
Start script at interactive mode
```
./start_install.py -i ipv6
```

## Known problems

1. Only Debian 8 with 3.* kernel at proxies nodes
2. Do not have interactive mode to ipv4 proxies only config file
3. Do not permit install ipv6 and ipv4 together.
