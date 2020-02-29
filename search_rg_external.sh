#!/bin/bash

# Author Github:   https://github.com/g666gle
# Author Twitter:  https://twitter.com/g666g1e
# Date: 12/4/2019
# Usage: ./search_rg_external.sh test@example.com /full/path/to/data/directory
# Usage: ./search_rg_external.sh test@ /full/path/to/data/directory
# Usage: ./search_rg_external.sh @example.com /full/path/to/data/directory
# Description:	


RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color


# Makes sure the user is in the BaseQuery dir
if [ "${PWD##*/}" == "BaseQuery" ];then
	# Grab everything before the @ sign
	user_name=$(echo "$1" | cut -d @ -f 1 | awk '{print tolower($0)}')
	email=$(echo "$1" | cut -d : -f 1 | awk '{print tolower($0)}')
	check_for_at=${1:0:1}

	# Check to see if the user entered in a domain ex) @google.com
	if [ "$check_for_at" == "@" ];then
		#  Make sure the given directory exists
		if [ -d "$2" ];then
			external_dir="$2"
			# If the last char is a '/' get rid of it
			if [ "${external_dir: -1}" == "/" ];then
				#  Delete the / and re-assign
				external_dir="${external_dir%?}"
			fi
			#  Check to see if the user gives the data/ dir or the parent dir to data
			check_data_dir="$(echo $external_dir | rev | cut -d '/' -f 1 | rev)"
			if [ "$check_data_dir" != "data" ];then
				printf "${RED}[!] Please provide the full path to the external data/ directory!${NC}\n"
				exit 0
			fi
			# If the data/ directory is not empty
			if [ "$(ls -A $external_dir)" ]; then
				read -p "Output to a file? [y/n] " out_to_file 
				# Checks input
				while [[ "$out_to_file" != [YyNn] ]];do
					printf "${YELLOW}[!]${NC} Please enter either \"y\" or \"n\"!\n"
					read -p "Output to a file? [y/n] " out_to_file 
				done

				timestamp="Null"
				metadata="Null"
				# Does the user want to output the results to a file
				if [[ "$out_to_file" == [Yy] ]];then
					# Make sure the outputfiles dir exists
					if ! [ -d ./OutputFiles ];then
						mkdir OutputFiles
					fi

					read -p "Do you want the outputed file to include a time-stamp? [y/n] " timestamp 
					# Checks input
					while [[ "$timestamp" != [YyNn] ]];do
						printf "${YELLOW}[!]${NC} Please enter either \"y\" or \"n\"!\n"
						read -p "Do you want the outputed file to include a time-stamp? [y/n] " timestamp 
					done

					read -p "Would you like the output to include metadata? [y/n] " metadata
					# Checks input
					while [[ "$metadata" != [YyNn] ]];do
						printf "${YELLOW}[!]${NC} Please enter either \"y\" or \"n\"!\n"
						read -p "Would you like the output to include metadata? [y/n] " metadata 
					done
					printf "${GREEN}[+]${NC} Outputting all results to ${GREEN}$(pwd)/OutputFiles/$1_output.txt${NC}\n"
					printf "${GREEN}[+]${NC} Please wait this could take a few minutes!\n"

				fi

				# Decompress all files
				printf "${GREEN}[+]${NC} Decompressing files\n"
				./decompress.sh -d "$external_dir"
				
				printf "${GREEN}[+]${NC} Starting search!\n"

				start=$SECONDS
				# check if the user wants the output to a file
				if [[ "$out_to_file" == [Yy] ]];then 
					#  check to see if the user wants to see metadata
					if [[ "$metadata" == [Yy] ]];then
						# The user wants timestamps
						if [[ "$timestamp" == [Yy] ]];then
							# add a time stamp
							printf "\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n\n" >>  ./OutputFiles/"$1"_output.txt
							printf "The results below were generated at:\n$(date)\n\n" >>  ./OutputFiles/"$1"_output.txt
							rg --ignore-case --color never --heading --line-number --stats $1 '$external_dir'  >> ./OutputFiles/"$1"_output.txt
							printf "\n" >> ./OutputFiles/"$1"_output.txt
						# The user doesn't want timestamps
						else
							rg --ignore-case --color never --heading --line-number --stats $1 '$external_dir' >> ./OutputFiles/"$1"_output.txt
							printf "\n" >> ./OutputFiles/"$1"_output.txt
						fi

					else
						# The user wants a time stamp but no metadata
						if [[ "$timestamp" == [Yy] ]];then
							# add a time stamp
							printf "\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n\n" >>  ./OutputFiles/"$1"_output.txt
							printf "The results below were generated at:\n$(date)\n\n" >>  ./OutputFiles/"$1"_output.txt
							echo "$(rg -iN --no-filename --no-heading $1 $external_dir)" >> ./OutputFiles/"$1"_output.txt
							printf "\n" >> ./OutputFiles/"$1"_output.txt
						# No timestamp and no meta data
						else
							echo "$(rg -iN --no-filename --no-heading $1 $external_dir)" >> ./OutputFiles/"$1"_output.txt
							printf "\n" >> ./OutputFiles/"$1"_output.txt
						fi

					fi 

				else # Send the output to the console
					#  check to see if the user wants to see metadata
					if [[ "$metadata" == [Yy] ]];then
						echo "$(rg -i $1 $external_dir)"
					# No metadata
					else
						echo "$(rg -iN --no-filename --no-heading $1 $external_dir | sed -e ''/:/s//$(printf '\033[0;31m:')/'' -e ''/$/s//$(printf '\033[0m')/'')"
					fi 
				fi
				stop=$SECONDS
				diff=$(( stop - start ))
				#  reading the number of uncompressed bytes in the data folder
				echo
				size_of_db_in_bytes=$(du -sb $external_dir'/' | cut -f 1)
				#  Multiplying the bytes to get GB (Note: I divide by 1 because 'bc' is annoying and wont round if you dont)
				size_of_db_in_gb=$(echo "scale=3; ($size_of_db_in_bytes * 0.000000001)"/1 | bc)
				printf "${YELLOW}[!]${NC} Searched through your ${GREEN}$size_of_db_in_gb GB ${NC}BaseQuery database in $diff seconds!\n"
				exit 0
			else
				printf "${RED}ERROR:${NC} $external_dir directory is empty please import files first!\n"
				exit 0
			fi
		else
			printf "${RED}ERROR:${NC} $2 directory does not exist!\n"
			exit 0
		fi
	fi # check for @

	#########################################################################
	# The above code deals with querying every file for a specific domain	#
	# The below code deals with querying a specific username or file	    #
	#########################################################################

	# Deals with all the cases of having a file vs stdout
	out_to_file="N"

	#  Ask the user if they want to output results
	read -p "Output to a file? [Y/N] " out_to_file 
	# Checks input
	while [[ "$out_to_file" != [YyNn] ]];do
		printf "${YELLOW}[!]${NC} Please enter either \"Y\" or \"N\"!\n"
		read -p "Output to a file? [Y/N] " out_to_file 
	done
	# Informing the user
	printf "${GREEN}[+]${NC} Starting search!\n"
	if [[ "$out_to_file" == [Yy] ]];then
		# Make the dir if it doesn't exist
		if ! [ -d ./OutputFiles ];then
			mkdir OutputFiles
		fi
		out_to_file="Y"
		printf "${GREEN}[+]${NC} Outputting all results to ${GREEN}./OutputFiles/$1_output.txt${NC}\n"
	fi

	#  Check to make sure the directory given exists and then store it in a var
	if [ -d "$2" ];then
		external_dir=$2
	else
		printf "${RED}[!]${NC} Directory $2 doesn't exist!"
		exit 1
	fi

	echo $1
	echo $2

	#  Check to make sure the user name is at least 4 and the email has a @
	if [[ ${#user_name} -ge 4 ]] && [[ "$email" == *"@"* ]];then	
		# Grab each individual character
		first_char=${user_name:0:1}  # ${variable name: starting position : how many letters}
		second_char=${user_name:1:1}
		third_char=${user_name:2:1}
		fourth_char=${user_name:3:1}
		
		#  Check to see if the folder is compressed
		if [ -e "$external_dir/$first_char".tar.zst ];then
			#  Decompress the data
			./decompress.sh -p "$external_dir/$first_char".tar.zst > /dev/null
		fi

		#  Check the first directory
		if [ -d "$external_dir/$first_char" ];then
			#  Check the second directory
			if [ -d  "$external_dir/$first_char"/"$second_char" ];then
				#  Check the third directory
				if [ -d "$external_dir/$first_char"/"$second_char"/"$third_char" ];then
					if [[ "$out_to_file" == [Nn] ]];then
						printf "${GREEN}Email Address: $email${NC}\n"
					fi
					#  Check to see if the file exists
					if [ -e "$external_dir/$first_char"/"$second_char"/"$third_char"/"$fourth_char".txt ];then
						#  Open the file and search for the email address then only keep the passwords, iterate through the passwords and echo then
						rg -iN --no-filename --no-heading --color never ^$email $external_dir/$first_char"/"$second_char"/"$third_char"/"$fourth_char.txt | while read -r Line;do
							user_name="$(echo $Line | cut -f 1 -d ':')"
							Password="$(echo $Line | cut -f 2- -d ':')"
							# check if the user wants the output to a file
							if [[ "$out_to_file" == [Yy] ]];then 
								echo  "$Line" >> ./OutputFiles/"$1"_output.txt
							else # Send the output to the console
								printf "$user_name${RED}:$Password${NC}\n"
							fi
						done
						
						#  Check to see if the email is in the NOT VALID file
						if [[ -d "$external_dir"/NOTVALID && -e "$external_dir"/NOTVALID/FAILED_TEST.txt ]];then
							rg -iN --no-filename --no-heading --color never "^$email $external_dir"/NOTVALID/FAILED_TEST.txt | while read -r Line;do
								user_name="$(echo $Line | cut -f 1 -d ':')"
								Password="$(echo $Line | cut -f 2- -d ':')"
								# check if the user wants the output to a file
								if [[ "$out_to_file" == [Yy] ]];then 
									echo  "$Line" >> ./OutputFiles/"$1"_output.txt
								else # Send the output to the console
									printf "$user_name${RED}:$Password${NC}\n"
								fi
							done	
						fi
					else
						#  The file does not exists
						#  Check to make sure the directory exists and the file exists for 0UTLIERS
						if [[ -d "$external_dir"/$first_char/$second_char/$third_char/0UTLIERS && -e "$external_dir"/$first_char/$second_char/$third_char/0UTLIERS/0utliers.txt ]];then
							rg -iN --no-filename --no-heading --color never ^$email $external_dir"/"$first_char"/"$second_char"/"$third_char/0UTLIERS/0utliers.txt | while read -r Line;do
								user_name="$(echo $Line | cut -f 1 -d ':')"
								Password="$(echo $Line | cut -f 2- -d ':')"
								# check if the user wants the output to a file
								if [[ "$out_to_file" == [Yy] ]];then 
									echo  "$Line" >> ./OutputFiles/"$1"_output.txt
								else # Send the output to the console
									printf "$user_name${RED}:$Password${NC}\n"
								fi
							done	
						fi

						#  Check to see if the email is in the NOT VALID file
						if [[ -d "$external_dir"/NOTVALID && -e "$external_dir"/NOTVALID/FAILED_TEST.txt ]];then
							rg -iN --no-filename --no-heading --color never ^$email $external_dir/NOTVALID/FAILED_TEST.txt | while read -r Line;do
								user_name="$(echo $Line | cut -f 1 -d ':')"
								Password="$(echo $Line | cut -f 2- -d ':')"
								# check if the user wants the output to a file
								if [[ "$out_to_file" == [Yy] ]];then 
									echo  "$Line" >> ./OutputFiles/"$1"_output.txt
								else # Send the output to the console
									printf "$user_name${RED}:$Password${NC}\n"
								fi
							done	
						fi					
					fi
				else
					if [[ "$out_to_file" == [Nn] ]];then
						printf "${GREEN}Email Address: "$email"${NC}\n"
					fi
					#  The third letter directory does not exists
					if [[ -d "$external_dir"/$first_char/$second_char/0UTLIERS && -e "$external_dir"/$first_char/$second_char/0UTLIERS/0utliers.txt ]];then
						rg -iN --no-filename --no-heading --color never ^$email $external_dir"/"$first_char"/"$second_char/0UTLIERS/0utliers.txt | while read -r Line;do
							user_name="$(echo $Line | cut -f 1 -d ':')"
							Password="$(echo $Line | cut -f 2- -d ':')"
							# check if the user wants the output to a file
							if [[ "$out_to_file" == [Yy] ]];then 
								echo  "$Line" >> ./OutputFiles/"$1"_output.txt
							else # Send the output to the console
								printf "$user_name${RED}:$Password${NC}\n"
							fi
						done	
					fi

					#  Check to see if the email is in the NOT VALID file
					if [[ -d "$external_dir"/NOTVALID && -e "$external_dir"/NOTVALID/FAILED_TEST.txt ]];then
						rg -iN --no-filename --no-heading --color never ^$email $external_dir/NOTVALID/FAILED_TEST.txt | while read -r Line;do
							user_name="$(echo $Line | cut -f 1 -d ':')"
							Password="$(echo $Line | cut -f 2- -d ':')"
							# check if the user wants the output to a file
							if [[ "$out_to_file" == [Yy] ]];then 
								echo  "$Line" >> ./OutputFiles/"$1"_output.txt
							else # Send the output to the console
								printf "$user_name${RED}:$Password${NC}\n"
							fi
						done	
					fi
				fi
			else
				if [[ "$out_to_file" == [Nn] ]];then
					printf "${GREEN}Email Address: "$email"${NC}\n"
				fi
				#  The second letter directory does not exists
				if [[ -d "$external_dir"/$first_char/0UTLIERS && -e "$external_dir"/$first_char/0UTLIERS/0utliers.txt ]];then
					rg -iN --no-filename --no-heading --color never ^$email $external_dir/$first_char/0UTLIERS/0utliers.txt | while read -r Line;do
						user_name="$(echo $Line | cut -f 1 -d ':')"
						Password="$(echo $Line | cut -f 2- -d ':')"
						# check if the user wants the output to a file
						if [[ "$out_to_file" == [Yy] ]];then 
							echo  "$Line" >> ./OutputFiles/"$1"_output.txt
						else # Send the output to the console
							printf "$user_name${RED}:$Password${NC}\n"
						fi
					done	
				fi

				#  Check to see if the email is in the NOT VALID file
				if [[ -d "$external_dir"/NOTVALID && -e "$external_dir"/NOTVALID/FAILED_TEST.txt ]];then
					rg -iN --no-filename --no-heading --color never ^$email $external_dir/NOTVALID/FAILED_TEST.txt | while read -r Line;do
						user_name="$(echo $Line | cut -f 1 -d ':')"
						Password="$(echo $Line | cut -f 2- -d ':')"
						# check if the user wants the output to a file
						if [[ "$out_to_file" == [Yy] ]];then 
							echo  "$Line" >> ./OutputFiles/"$1"_output.txt
						else # Send the output to the console
							printf "$user_name${RED}:$Password${NC}\n"
						fi
					done	
				fi
			fi
		else
			if [[ "$out_to_file" == [Nn] ]];then
				printf "${GREEN}Email Address: "$email"${NC}\n"
			fi
			#  The first letter directory does not exists
			if [[ -d "$external_dir"/0UTLIERS && -e "$external_dir"/0UTLIERS/0utliers.txt ]];then
				rg -iN --no-filename --no-heading --color never ^$email $external_dir/0UTLIERS/0utliers.txt | while read -r Line;do
					user_name="$(echo $Line | cut -f 1 -d ':')"
					Password="$(echo $Line | cut -f 2- -d ':')"
					# check if the user wants the output to a file
					if [[ "$out_to_file" == [Yy] ]];then 
						echo  "$Line" >> ./OutputFiles/"$1"_output.txt
					else # Send the output to the console
						printf "$user_name${RED}:$Password${NC}\n"
					fi
				done	
			fi

			#  Check to see if the email is in the NOT VALID file
			if [[ -d "$external_dir"/NOTVALID && -e "$external_dir"/NOTVALID/FAILED_TEST.txt ]];then
				rg -iN --no-filename --no-heading --color never "^$email" "$external_dir"/NOTVALID/FAILED_TEST.txt | while read -r Line;do
					user_name="$(echo $Line | cut -f 1 -d ':')"
					Password="$(echo $Line | cut -f 2- -d ':')"
					# check if the user wants the output to a file
					if [[ "$out_to_file" == [Yy] ]];then 
						echo  "$Line" >> ./OutputFiles/"$1"_output.txt
					else # Send the output to the console
						printf "$user_name${RED}:$Password${NC}\n"
					fi
				done	
			fi
		fi
	else  # If not a valid address
		first_char=${user_name:0:1}  # {variable name: starting position : how many letters}

		#  Check to see if the folder is compressed
		if [ -e "$external_dir"/"$first_char".tar.zst ];then
			./decompress.sh -p "$first_char".tar.zst > /dev/null
		fi
		#  Uncompresses NOTVALID
		if [ -e "$external_dir"/NOTVALID.tar.zst ];then
			./decompress.sh -p NOTVALID.tar.zst > /dev/null
		fi
		# Supreses output
		if [[ "$out_to_file" == [Nn] ]];then
			printf "${GREEN}Email Address: "$email"${NC}\n"
		fi

		# Checks if the email has an @ 
		if [[ $email == *"@"* ]];then
			#  The username is either not >= 4 or the email doesn't contain an @
			#  Check to see if the email is in the NOT VALID file
			if [[ -d "$external_dir"/NOTVALID && -e "$external_dir"/NOTVALID/FAILED_TEST.txt ]];then
				rg -iN --no-filename --no-heading --color never ^$email $external_dir/NOTVALID/FAILED_TEST.txt | while read -r Line;do
					user_name="$(echo $Line | cut -f 1 -d ':')"
					Password="$(echo $Line | cut -f 2- -d ':')"
					# check if the user wants the output to a file
					if [[ "$out_to_file" == [Yy] ]];then 
						echo  "$Line" >> ./OutputFiles/"$1"_output.txt
					else # Send the output to the console
						printf "$user_name${RED}:$Password${NC}\n"
					fi
				done	
			fi
		else
			printf "${YELLOW}[!]${NC} Please enter one email address or a file with one email address per line\n"
		fi
	fi # end of valid email check

else
	printf "${RED}ERROR: Please change directories to the BaseQuery root directory${NC}\n"
fi





