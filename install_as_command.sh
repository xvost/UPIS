#!/bin/bash
# Required docker
# if you need non-root work configure docker to non-root work

docker build -t upis:latest .
mkdir -p ~/.local/bin
cp ./upis.sh ~/.local/bin/upis
chmod +x ~/.local/bin/upis
