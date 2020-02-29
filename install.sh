#!/bin/bash

# Author Github:   https://github.com/g666gle
# Author Twitter:  https://twitter.com/g666g1e
# Date: 12/9/2019
# Usage: ./install.sh
# Description:	This script when run first checks to make sure that the user is
#		in the correct directory. Then, when provided with sudo privledges
#		it will install all dependencies needed to properly run BaseQuery.

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Color


# Check if the user is running as root
# the person could either be using sudo or is root
if [ "$EUID" -eq 0 ]; then
	# Check to see if you are in the BaseQuery directory
	if [ "${PWD##*/}" == "BaseQuery" ];then
		echo "export TERM=xterm"  >> ~/.bashrc
		export DEBIAN_FRONTEND=noninteractive
		export PATH=/root/.local/bin:$PATH
		# This runs a simple to check for sudo and if it is downloaded is should ask for a pwd
		CAN_I_RUN_SUDO=$(sudo -n true 2>&1 | grep "a password is required" | wc -l)
		# Now we do the same check but without the pipes to allow it to return a non 0 exit code
		CHECK_EXIT_CODE=$(sudo -n true 2>1)
		# This grabs the exit code of the previous command (0 means no errors)
		EXIT_CODE=$(echo $?)
		# Checks to see if you can run sudo or a password is required for sudo
		# If the person already logged in as sudo CHECK_EXIT_CODE will return nothing
		if [[ $EXIT_CODE -eq 0 || $CAN_I_RUN_SUDO -gt 0 ]]; then
			#  If this is the case the person is using sudo
			sudo chmod 755 -R $(pwd)
			printf "${GREEN}[+] Updating apt-get${NC}\n"
			sudo apt-get update -y 1> /dev/null
			printf "${GREEN}[+] Installing apt-utils${NC}\n"
			sudo apt-get install ca-certificates dialog apt-utils -y > /dev/null 2>&1
			printf "${GREEN}[+] Adding ripgrep repository${NC}\n"
			sudo apt-get install software-properties-common -y > /dev/null 2>&1
			sudo add-apt-repository ppa:x4121/ripgrep -y > /dev/null 2>&1
			printf "${GREEN}[+] Installing Python3.7-minimal${NC}\n"
			sudo apt-get install python3.7-minimal -y 1> /dev/null
			printf "${GREEN}[+] Installing Python3-pip${NC}\n"
			sudo apt-get install python3-pip -y 1> /dev/null
			printf "${GREEN}[+] Installing tar${NC}\n"
			sudo apt-get install tar -y 1> /dev/null
			printf "${GREEN}[+] Installing zstd${NC}\n"
			sudo apt-get install zstd -y 1> /dev/null
			printf "${GREEN}[+] Installing xterm${NC}\n"
			sudo apt-get install xterm -y 1> /dev/null
			printf "${GREEN}[+] Installing ripgrep${NC}\n"
			sudo apt-get install ripgrep -y 1> /dev/null
			printf "${GREEN}[+] Installing bc${NC}\n"
			sudo apt-get install bc -y 1> /dev/null
			printf "${GREEN}[+] Installing requirements.txt${NC}\n"
			pip3 install -r requirements.txt --user

		else
			#  If this is the case the person is logged in as root 
			#  but doesn't have sudo installed
			chmod 755 -R $(pwd)
			printf "${GREEN}[+] Updating apt-get${NC}\n"
			apt-get update -y 1> /dev/null
			printf "${GREEN}[+] Installing apt-utils${NC}\n"
			apt-get install ca-certificates dialog apt-utils -y > /dev/null 2>&1
			printf "${GREEN}[+] Adding ripgrep repository${NC}\n"
			apt-get install software-properties-common -y > /dev/null 2>&1
			add-apt-repository ppa:x4121/ripgrep -y > /dev/null 2>&1
			printf "${GREEN}[+] Installing Python3.7-minimal${NC}\n"
			apt-get install python3.7-minimal -y 1> /dev/null
			printf "${GREEN}[+] Installing Python3-pip${NC}\n"
			apt-get install python3-pip -y 1> /dev/null
			printf "${GREEN}[+] Installing tar${NC}\n"
			apt-get install tar -y 1> /dev/null
			printf "${GREEN}[+] Installing zstd${NC}\n"
			apt-get install zstd -y 1> /dev/null
			printf "${GREEN}[+] Installing xterm${NC}\n"
			apt-get install xterm -y 1> /dev/null
			printf "${GREEN}[+] Installing ripgrep${NC}\n"
			apt-get install ripgrep -y 1> /dev/null
			printf "${GREEN}[+] Installing bc${NC}\n"
			apt-get install bc -y  1> /dev/null
			printf "${GREEN}[+] Installing requirements.txt${NC}\n"
			pip3 install -r requirements.txt  --user
		fi

		if [[ -e ./Logs/temp_benchmark_DB/data/DELETE_ME.txt ]];then
			rm -f ./Logs/temp_benchmark_DB/data/DELETE_ME.txt
		fi

		if [[ -e ./OutputFiles/DELETE_ME.txt ]];then
			rm -f ./OutputFiles/DELETE_ME.txt
		fi

		if [[ -e ./data/DELETE_ME.txt ]];then
			rm -f ./data/DELETE_ME.txt
		fi
		if [[ -e ./PutYourDataBasesHere/example.txt ]];then
			rm -f ./PutYourDataBasesHere/example.txt
		fi

		echo
		printf "${GREEN}[+]${NC} Finished downloading!${NC}\n"
	else
		printf "${RED}ERROR: Please change directories to the BaseQuery root directory${NC}\n"
	fi
	exit
fi

printf "${RED}ERROR: Please run this script as root using \"sudo ./install.sh\"\n"
exit




