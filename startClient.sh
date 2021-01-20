#! /bin/bash
sudo docker build . -t imageclient
sudo docker build . -t imageserver -f Dockerfile_server
sudo docker run -p 3000:5000 --rm -it imageclient 
