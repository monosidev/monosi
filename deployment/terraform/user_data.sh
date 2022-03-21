#!/bin/bash

sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo usermod -a -G docker $USER

mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo mv ~/.docker/cli-plugins/docker-compose /usr/local/lib/docker/cli-plugins/docker-compose

sudo yum install -y git
git clone https://github.com/monosidev/monosi

cd monosi
sudo make compose

