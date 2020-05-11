#!/bin/bash

# install and check for gcc
sudo apt-get -y install build-essential

# install cmake
sudo apt-get -y install cmake

# check and install souffle
if [ $(dpkg-query -W -f='${Status}' souffle 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	  the_ppa="https://dl.bintray.com/souffle-lang/deb-unstable bionic main"

	  if ! grep -q "^deb .*$the_ppa" /etc/apt/sources.list; 
	  then
		echo "deb https://dl.bintray.com/souffle-lang/deb-unstable bionic main" | sudo tee -a /etc/apt/sources.list
	  fi

	  sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61
	  sudo apt-get update
	  sudo apt-get -y install souffle
fi

# install python
sudo apt-get install python3

# get boost libraries
sudo apt-get -y install libpthread-workqueue0 libboost-all-dev

