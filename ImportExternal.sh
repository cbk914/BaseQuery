#!/bin/bash

# Author Github:   https://github.com/g666gle
# Author Twitter:  https://twitter.com/g666g1e
# Date: 12/1/2019
# Usage: ./ImportExternal <Full path to import data from> (This will export data to default data dir)
# Usage: ./ImportExternal <Full path to import data from> <Full path to export data to> 
# Description:	ImportExternal.sh first checks to make sure the user is in the correct directory.
#		Then, every file in the data directory will have their hash compared to the
#		log file keeping track of all of the databases previously imported. If the
#		database has not been previously imported, the data is decompressed and the
#		folder is primed, lastly the pysort.py file is called. This file is a slight 
#		modification from Import.sh and makes the proper adjustments to deal with external locations
#		used to import files.

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Color

printf "${RED}[*]${NC} Starting at $(date)\n"

#Checks to see if the user is working out of the BaseQuery directory
if [ "${PWD##*/}" == "BaseQuery" ];then
	if [ $# -eq 1 ] || [ $# -eq 2 ];then
		#  Checks to see if the Import directory is there
		if [ -d $1 ];then
			#  Set the datadir to be the passed in path
			dataDir="$1"
			#The users pathe to the basequery directory
			pwd=$(pwd)

			#  This loop is checking to see if any new files are in the data
			#  directory.If not then there is no reason to decompress and compress everything
			let i=0  # used to count the amount of files not already imported
			declare -a arr
			 while read -r inputfile;do
				arr=(${inputfile})
				file_SHA_sum="$(sha256sum "$inputfile" | awk '{print$1}')"
				#  check to see if the database has already been imported
				if [ "$(rg $file_SHA_sum -c $pwd/Logs/importedDBS.log)" == "" ];then
					let i=i+1
				fi
				_constr+="${arr[2]}"
			done< <(find $dataDir -type f -exec echo {} \;)

			# if there are files that need to be imported
			if [ $i -ne 0 ];then
				#  decompress all of the folders before priming and import
				printf "${YELLOW}[!]${NC} Decompressing all stored data\n"
				printf "[!] Decompressing all stored data\n" >> "$pwd"/Logs/ActivityLogs.log
				#  If there are 2 args given then an export path is given
				if [ $# -eq 2 ]; then
					./decompress.sh -d "$2"
				# Use default export path
				elif [ $# -eq 1 ]; then
					./decompress.sh
				fi
				printf "${GREEN}[+]${NC} Finished decompressing!\n"
				printf "[+] Finished decompressing!\n" >> "$pwd"/Logs/ActivityLogs.log

				# Prime the given export path
				if [ $# -eq 2 ]; then
					#  Prime the data folder
					python3 folderPrimer.py "$2"
				# Prime the default export dir
				elif [ $# -eq 1 ]; then
					#  Prime the data folder
					python3 folderPrimer.py
				fi

				#  Read each file in the input files, in sorted order
				find $dataDir -type f -exec echo {} \; | while read -r inputfile;do
					file_SHA_sum="$(sha256sum "$inputfile" | awk '{print$1}')"
					#  check to see if the database has already been imported
					if [ "$(rg $file_SHA_sum -c ./Logs/importedDBS.log)" == "" ];then
						# Gets the file name from the full path
						name=$(echo $inputfile | rev | cut -d'/' -f 1 | rev)
						# Grabs the full path excluding the filename
						dir=$(echo $inputfile | rev | cut -d'/' -f 2- | rev)

						#  Checks to see if a input dir and export dir are given
						if [ $# -eq 3 ];then
							#  Sort file from somewhere else and export somewhere else
							python3 pysort.py --export_dir "$2" --input_dir "$dir" "$inputfile" 
						else
							#  Call a python script to iterate through the file and sort them
							python3 pysort.py --input_dir "$dir" "$inputfile"
						fi
						printf "${YELLOW}[!] Adding $inputfile to importedDBS.log${NC}\n"
						echo "$file_SHA_sum" "$(date)" "$inputfile" >> "$pwd"/Logs/importedDBS.log
						echo
					else
						printf "${YELLOW}[!]${NC} $inputfile SHASUM found in importedDBS.log\n"
						printf "[!] $inputfile SHASUM found in importedDBS.log\n" >> "$pwd"/Logs/ActivityLogs.log
					fi
				done
				printf "${YELLOW}[!]${NC} Compressing all data\n"
				printf "[!] Compressing all data\n" >> "$pwd"/Logs/ActivityLogs.log

				#  All data is stored. Time to compress
				if [ $# -eq 2 ];then
					./compress.sh "$2"
				# Use default export path
				elif [ $# -eq 1 ];then
					./compress.sh
				fi

				printf "${GREEN}[+]${NC} Finished compressing!\n"
				printf "[+] Finished compressing!\n" >> "$pwd"/Logs/ActivityLogs.log

			else # No new files found
				echo
				printf "${RED}ERROR:${NC} No new files found in the 'PutYourDataBasesHere' directory \n"
				printf "ERROR: No new files found in the 'PutYourDataBasesHere' directory \n" >> "$pwd"/Logs/ActivityLogs.log

			fi # check for imported files

		else    #  If the Import directory doesn't exist
			dataDir=$(pwd)
			printf "${RED}ERROR: The given directory does not exist${NC}\n"
			printf "ERROR: The given directory does not exist\n" >> "$pwd"/Logs/ActivityLogs.log
		fi
	else
		printf "${RED}ERROR: Wrong amount of arguments given${NC}\n"
		printf "${RED}ERROR: Wrong amount of arguments given${NC}\n" >> "$pwd"/Logs/ActivityLogs.log
	fi
else
	# If the users working directory is not BaseQuery while trying to run the script
	printf "${RED}ERROR: Please change directories to the BaseQuery root directory${NC}\n"
	printf "ERROR: Please change directories to the BaseQuery root directory\n" >> "$pwd"/Logs/ActivityLogs.log
fi

echo
printf "${RED}[*]${NC} Completed\n"
echo "[*] Completed\n" >> "$pwd"/Logs/ActivityLogs.log

