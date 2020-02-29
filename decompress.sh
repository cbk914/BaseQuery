#!/bin/bash

# Author Github:   https://github.com/g666gle
# Author Twitter:  https://twitter.com/g666g1e
# Date: 12/1/2019
# Usage:   ./decompress.sh  (This decompresses everything in the default data/ in BaseQuery)
# Usage:   ./decompress.sh -f <name of compressed file>  (This file must be within the data/ directory)
# Usage:   ./decompress.sh -p <full path to compressed file>  (This file can be anywhere on disk)
# Usage:   ./decompress.sh -d <directory path>  (This directory can be anywhere on disk)
# Description:	This script first checks to make sure that the user is in the correct directory.
#		You can either just run the script with no parameters, which will decompress all
#		files within the default data directory. Or you can provide the name of a file, anywhere on disk,
#		using the -f flag. You also can provide a directory to decompress using the -d flag.


RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

#  Make sure the user is in the BaseQuery directory
if [ "${PWD##*/}" == "BaseQuery" ];then
	#  Check if no args were passed in; then decompress everything
	if [ $# -eq 0 ];then
		#  Iterate through all the compressed files 
		find data/ -type f -name "*.tar.zst" | sort | while read -r compressed_file; do
			#  check to make sure you dont decompress the working directory
			if [ "$compressed_file" != "data/" ];then
				#  Grabs the name of the file from the path
				name="$(echo $compressed_file | cut -f 2- -d "/" | cut -f 1 -d '.')"
				# decompress the .tar.zst files
				tar --use-compress-program=zstd -xf ./data/$name.tar.zst && rm -rf data/"$name".tar.zst				
			fi	
		done
	#  Decompress a specific file outside of the BaseQuery dir
	elif [ $# -eq 2 ];then
		while getopts "f:d:p:" opt; do
		  case $opt in
		    d )
				#  Check if were given a valid directory
				if [ -d $OPTARG ]; then
					#  Checks to see if the directory is not empty ( if empty nothing to decompress )
					if [ "$(ls -A $OPTARG)" ]; then
						# Iterate through all of the compressed archives in the supplied dir
						find "$OPTARG" -type f -name "*.tar.zst" | sort | while read -r compressed_file; do
							file_name_with_extentions=$(echo "$compressed_file" | rev | cut -d '/' -f 1 | rev)
							# get the name of the file without any extentions. This is needed to specify the directory
							file_name_no_extention=$(echo "$file_name_with_extentions"| cut  -d '.' -f 1)
							#  Decompress the archive [error sent to dev null to supress a warrning about removing leading '/']
							#echo tar --use-compress-program=zstd -xf "$compressed_file" -C "$OPTARG" --one-top-level="$file_name_no_extention" 2> /dev/null && rm -rf "$compressed_file"
							tar --use-compress-program=zstd -xf $compressed_file -C $OPTARG 2> /dev/null && rm -rf $compressed_file
						done
					fi
				else
					printf "${RED}[!]${NC} Directory '$OPTARG' doesn't exist!\n"
				fi
				exit
				;;
			f )
				# make sur you dont try and decompress the working directory
				if [ "$OPTARG" != "data/" ];then
					if [ -f ./data/"$OPTARG" ];then
						# decompress the .tar.zst files
						#tar --use-compress-program=zstd -xf ./data/0.tar.zst
						tar --use-compress-program=zstd -xf ./data/"$OPTARG" && rm -rf data/"$1"	
					else
						printf "${RED}[!]${NC} File ./data/'$OPTARG' not found!\n"
						exit 1
					fi
				fi
				exit
				;;
			p )
				if [ -f "$OPTARG" ];then
					#  This strips away the file from the full path
					directory_path="$(dirname $OPTARG)"
					# decompress the .tar.zst file
					tar --use-compress-program=zstd -xf $OPTARG -C $directory_path && rm -rf $OPTARG	
				else
					printf "${RED}[!]${NC} File $OPTARG not found!\n"
					exit 1
				fi

				exit
				;;
		    \?)
				echo "Invalid option: -$OPTARG" >&2
				printf "${RED}[!]${NC} Usage Error: ./decompress.sh  (This decompresses everything in the default data/ in BaseQuery) \n"
				printf "${RED}[!]${NC} Usage Error: ./decompress.sh -f <name of compressed file>  (This file must be within the data/ directory)\n"
				printf "${RED}[!]${NC} Usage Error: ./decompress.sh -d <directory path>  (This file can be anywhere on disk)\n"
				
				printf "[!] Usage Error: \n" >> ./Logs/ActivityLogs.log
				exit 1
				;;
      		esac
      	done

	else  # Wrong input
		printf "${RED}[!]${NC} Usage Error: ./decompress.sh  (This decompresses everything in the default data/ in BaseQuery) \n"
		printf "${RED}[!]${NC} Usage Error: ./decompress.sh -f <name of compressed file>  (This file must be within the data/ directory)\n"
		printf "${RED}[!]${NC} Usage Error: ./decompress.sh -d <directory path>  (This file can be anywhere on disk)\n"
		
		printf "[!] Usage Error: \n" >> ./Logs/ActivityLogs.log
		exit 1
		
	fi
else
	# If the users working directory is not BaseQuery while trying to run the script
	printf "${RED}ERROR: Please change directories to the BaseQuery root directory${NC}\n"
	printf "ERROR: Please change directories to the BaseQuery root directory\n" >> ./Logs/ActivityLogs.log
	exit 1
fi # Inside BaseQuery
