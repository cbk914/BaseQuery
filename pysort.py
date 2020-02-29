#!/usr/bin/env python3.7

try:
    import os
    import time
    import mmap
    #from ripgrepy import Ripgrepy
    import argparse
    #import subprocess
except Exception as e:
    print(e)
    exit(1)

"""
Author Github:   https://github.com/g666gle
Author Twitter:  https://twitter.com/g666g1e
Date:            12/1/2019
Description:     Takes in one file at a time as command line input. processes each line in the file and places the
                 information into the correct subdirectory of the data folder.
Usage:           python3 pysort.py file.txt 
Usage:           python3 pysort.py --input_dir /home/user/Desktop/databases file.txt
Usage:           python3 pysort.py --export_dir /home/user/Desktop file.txt
Usage:           python3 pysort.py --input_dir /home/user/Desktop/databases --export_dir /home/user/Desktop/ file.txt
Version:	     2.0.0
Python Version:  3.7.1
"""

# Need TODO
#TODO Make a docker instance
# Create a low hard drive space mode where when searching for lets say @gmail.com it would decompress 'a.tar.zst' search it and then recompress it after its done
# this way only one archive is decompressed at a time
#
# Add option for outputting meta data to console for queries besides @gamil
# have multiple log files for different storage places 
# Maybe try to use cython to speed up import
# use only dirs that are not compressed in byte statistics comprress.sh
# Export all data to a create sql file
# Option to choose certain dirs to check for @gmail.com
# Automatically find the amount of lines in import using wc
# have a check to make sure a file  exists before compressing or decompressing.sh


def check_duplicate(full_file_path: str, line: str) -> bool:
    """
    This function takes in a path to the file and the specific line we want to check for duplicates with. First the file
    is checked to make sure it isn't empty, then the file is opened as a binary so we can store the lines as a mmap obj.
    Next if the line is a duplicate then False is returned else True
    :param full_file_path: Path to the file
    :param line: The line being checked
    :return: True if the line should be written to the file; else False
    """

    ##########################################################
    # MY FAILED ATTEMPT AT USING RIPGREP TO SEARCH. AVG TIME #
    # WAS 100X SLOWER THAN MY MMAP IMPLEMENTATION BELOW      #
    ##########################################################

    # if os.getcwd().split('/')[-1] == 'BaseQuery':
    #     if not os.stat(full_file_path).st_size == 0:
    #         # Check to see if the line doesn't exist in the file
    #         rg = Ripgrepy(str(line.lower()), str(full_file_path)).count_matches().run().as_string
    #         if rg == "0" or rg == "":
    #             return True  # Write to the file
    #         else:
    #             return False  # string is in file so do not re-write it
    #     return True  # Write to the file
    # else:
    #     print("ERROR: Please run from within the BaseQuery directory")
    #     exit(1)
    #     #ERROR

    #  Check to see if the file is not empty
    if not os.stat(full_file_path).st_size == 0:
        #  Open the file as a binary file and store it in a mmap obj
        with open(full_file_path, 'rb', 0) as fp, mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ) as s:
            #  Check to see if the line already exists in the file
            if s.find(str.encode(line)) != -1:
                return False  # string is in file so do not re-write it
            return True  # string is not in file so write it to the file
    return True  # Write to the file


def place_data(line: str, path: str) -> int:
    """
    This function takes in the line of the current file and the root path to the BaseQuery directory. Checks the format
    of the file to make sure each line is in the email:password format. Then determines the depth of the correct characters
    ex) ex|ample@gmail.com  ---> would result in a depth of 2.  Then checking each directory to see if it already exists
    the username:password combo is correctly placed into a easy to query file. If a invalid character is determined in the
    first 4 chars then it will be put in a '0UTLIERS.txt' file.
    :param line: email:password
    :param path: full path to BaseQuery directory
    :return: Either a 1 or a 0 depending on if a line has been written or not
    """
    #  Check if the line starts with a :
    if line[0] == ":":
        #  strip the colon from the line
        line = line[1:]
    emailPaswd = line.split(':', 2)

    #  Checks to see if the users format is "Password:Username" instead of "Username:Password"
    if len(emailPaswd) >= 2 and '@' in emailPaswd[1] and '.' in emailPaswd[1]:
        #  Switches the position of the username and password
        temp = emailPaswd[0]
        emailPaswd[0] = emailPaswd[1].lower()
        emailPaswd[1] = temp
    else:
        #  Change all of the email usernames to be lowercase; to be uniform
        emailPaswd[0] = emailPaswd[0].lower()

    try:
        #  check to see if you have a valid email address and the username is >= 4; also checks if there is a '@' in the username
        if '@' in emailPaswd[0].strip() and len(emailPaswd[0].strip().split('@')[0]) >= 4 and len(emailPaswd) >= 2 and emailPaswd[0].strip().count('@') == 1:
            first_letter =  emailPaswd[0][0]
            second_letter = emailPaswd[0][1]
            third_letter =  emailPaswd[0][2]
            fourth_letter = emailPaswd[0][3]

            #  Check to see if the username has an invalid character and at what spot
            if str(first_letter).isalnum():
                folder_depth = 1
                if str(second_letter).isalnum():
                    folder_depth = 2
                    if str(third_letter).isalnum():
                        folder_depth = 3
                        if str(fourth_letter).isalnum():
                            folder_depth = 4
            else:
                folder_depth = 0

            # Make sure the user did not delete the data directory
            if not os.path.isdir(path + '/data/'):
                os.makedirs(path + '/data/')

            #  Check to see if the first letter doesn't have a directory
            if not os.path.isdir(path + "/data/" + first_letter):
                #  Check to see if we start with at least one valid char
                if folder_depth >= 1:
                    #  Make the directory
                    os.makedirs(path + "/data/" + first_letter)
                else:
                    #  If the outlier dir doesn't exist; make it and start the file
                    if not os.path.isdir(path + "/data/0UTLIERS"):
                        os.makedirs(path + "/data/0UTLIERS")
                        #  Don't need to check for duplicates because its a new file
                        with open(path + "/data/0UTLIERS/0utliers.txt", 'a') as fp:
                            length = len(emailPaswd)
                            #  Iterate through each index of the list and write it to the file
                            for index in range(length):
                                if index != length - 1:
                                    fp.write(emailPaswd[index] + ":")
                                else:  # Don't add a ':' at the end of the line
                                    fp.write(emailPaswd[index])
                            fp.write("\n")
                        return 1
                    else:  # If the outlier dir already exists append the line to the file
                        #  Get the new line from the emailPasswd list
                        length = len(emailPaswd)
                        new_line = ""
                        #  Iterate through each index and add it to new_line
                        for index in range(length):
                            if index != length - 1:
                                new_line += emailPaswd[index] + ":"
                            else:
                                new_line += emailPaswd[index]

                        if check_duplicate(path + "/data/0UTLIERS/0utliers.txt", new_line):
                            # Checks to see if there are duplicates already in the file, returns true if there isn't
                            with open(path + "/data/0UTLIERS/0utliers.txt", 'a') as fp:
                                fp.write(new_line + "\n")
                            return 1
                    return 0
            else:  # The directory already exists
                if folder_depth == 0:  # There is NOT at least one consecutive valid char
                    #  If the outlier dir doesn't exist; make it and start the file
                    if not os.path.isdir(path + "/data/0UTLIERS"):
                        os.makedirs("mkdir " + path + "/data/0UTLIERS")
                        with open(path + "/data/0UTLIERS/0utliers.txt", 'a') as fp:
                            length = len(emailPaswd)
                            #  Iterate through each index of the list and write it to the file
                            for index in range(length):
                                if index != length - 1:
                                    fp.write(emailPaswd[index] + ":")
                                else:  # Don't add a ':' at the end of the line
                                    fp.write(emailPaswd[index])
                            fp.write("\n")
                        return 1
                    else:  # If the outlier dir already exists append the line to the file
                        #  Get the new line from the emailPasswd list
                        length = len(emailPaswd)
                        new_line = ""
                        #  Iterate through each index and add it to new_line
                        for index in range(length):
                            if index != length - 1:
                                new_line += emailPaswd[index] + ":"
                            else:
                                new_line += emailPaswd[index]

                        if check_duplicate(path + "/data/0UTLIERS/0utliers.txt", new_line):
                            with open(path + "/data/0UTLIERS/0utliers.txt", 'a') as fp:
                                #  Write to the file
                                fp.write(new_line + "\n")
                            return 1
                    return 0

            #  Check to see if the second letter doesn't have a directory
            if not os.path.isdir(path + "/data/" + first_letter + "/" + second_letter):
                #  Check to see if we start with at least two valid char
                if folder_depth >= 2:
                    #  Make the directory
                    os.makedirs(path + "/data/" + first_letter + "/" + second_letter)
                else:
                    #  If the outlier dir doesn't exist; make it and start the file
                    if not os.path.isdir(path + "/data/" + first_letter + "/0UTLIERS"):
                        os.makedirs(path + "/data/" + first_letter + "/0UTLIERS")
                        with open(path + "/data/" + first_letter + "/0UTLIERS/0utliers.txt", 'a') as fp:
                            length = len(emailPaswd)
                            #  Iterate through each index of the list and write it to the file
                            for index in range(length):
                                if index != length - 1:
                                    fp.write(emailPaswd[index] + ":")
                                else:  # Don't add a ':' at the end of the line
                                    fp.write(emailPaswd[index])
                            fp.write("\n")
                        return 1
                    else:
                        #  Get the new line from the emailPasswd list
                        length = len(emailPaswd)
                        new_line = ""
                        #  Iterate through each index and add it to new_line
                        for index in range(length):
                            if index != length - 1:
                                new_line += emailPaswd[index] + ":"
                            else:
                                new_line += emailPaswd[index]

                        #  Check for duplicates
                        if check_duplicate(path + "/data/" + first_letter + "/0UTLIERS/0utliers.txt", new_line):
                            with open(path + "/data/" + first_letter + "/0UTLIERS/0utliers.txt", 'a') as fp:
                                fp.write(new_line + "\n")
                            return 1
                    return 0
            else:  # The directory already exists
                if folder_depth <= 1:  # There is not at least two consecutive valid char
                    #  If the outlier dir doesn't exist; make it and start the file
                    if not os.path.isdir(path + "/data/" + first_letter + "/0UTLIERS"):
                        os.makedirs(path + "/data/" + first_letter + "/0UTLIERS")
                        with open(path + "/data/" + first_letter + "/0UTLIERS/0utliers.txt", 'a') as fp:
                            length = len(emailPaswd)
                            #  Iterate through each index of the list and write it to the file
                            for index in range(length):
                                if index != length - 1:
                                    fp.write(emailPaswd[index] + ":")
                                else:  # Don't add a ':' at the end of the line
                                    fp.write(emailPaswd[index])
                            fp.write("\n")
                        return 1
                    else:  # If the outlier dir already exists append the line to the file
                        #  Get the new line from the emailPasswd list
                        length = len(emailPaswd)
                        new_line = ""
                        #  Iterate through each index and add it to new_line
                        for index in range(length):
                            if index != length - 1:
                                new_line += emailPaswd[index] + ":"
                            else:
                                new_line += emailPaswd[index]

                        if check_duplicate(path + "/data/" + first_letter + "/0UTLIERS/0utliers.txt", new_line):
                            with open(path + "/data/" + first_letter + "/0UTLIERS/0utliers.txt", 'a') as fp:
                                fp.write(new_line + "\n")
                            return 1
                    return 0

            #  Check to see if the third letter doesn't have a directory
            if not os.path.isdir(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter):
                #  Check to see if we start with at least three valid char
                if folder_depth >= 3:
                    #  Make the directory
                    os.makedirs(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter)
                else:
                    if not os.path.isdir(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS"):
                        os.makedirs(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS")
                        with open(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS/0utliers.txt", 'a') as fp:
                            length = len(emailPaswd)
                            #  Iterate through each index of the list and write it to the file
                            for index in range(length):
                                if index != length - 1:
                                    fp.write(emailPaswd[index] + ":")
                                else:  # Don't add a ':' at the end of the line
                                    fp.write(emailPaswd[index])
                            fp.write("\n")
                        return 1
                    else:  # If the outlier dir already exists append the line to the file
                        #  Get the new line from the emailPasswd list
                        length = len(emailPaswd)
                        new_line = ""
                        #  Iterate through each index and add it to new_line
                        for index in range(length):
                            if index != length - 1:
                                new_line += emailPaswd[index] + ":"
                            else:
                                new_line += emailPaswd[index]

                        if check_duplicate(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS/0utliers.txt", new_line):
                            with open(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS/0utliers.txt", 'a') as fp:
                                fp.write(new_line + "\n")
                            return 1
                    return 0
            else:  # The directory already exists
                if folder_depth <= 2:  # There is not at least three consecutive valid char
                    #  If the outlier dir doesn't exist; make it and start the file
                    if not os.path.isdir(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS"):
                        os.makedirs(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS")
                        with open(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS/0utliers.txt", 'a') as fp:
                            length = len(emailPaswd)
                            #  Iterate through each index of the list and write it to the file
                            for index in range(length):
                                if index != length - 1:
                                    fp.write(emailPaswd[index] + ":")
                                else:  # Don't add a ':' at the end of the line
                                    fp.write(emailPaswd[index])
                            fp.write("\n")
                        return 1
                    else:  # If the outlier dir already exists append the line to the file
                        #  Get the new line from the emailPasswd list
                        length = len(emailPaswd)
                        new_line = ""
                        #  Iterate through each index and add it to new_line
                        for index in range(length):
                            if index != length - 1:
                                new_line += emailPaswd[index] + ":"
                            else:
                                new_line += emailPaswd[index]

                        if check_duplicate(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS/0utliers.txt", new_line):
                            with open(path + "/data/" + first_letter + "/" + second_letter + "/0UTLIERS/0utliers.txt", 'a') as fp:
                                fp.write(new_line + "\n")
                            return 1
                    return 0

            #  Checks to see if the file in the third directory doesn't exists
            if not os.path.isfile(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/" + fourth_letter + ".txt"):
                if folder_depth == 4:  # The file doesn't exist in the third dir but there is 4 valid chars
                    #  Make the file
                    with open(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/" + fourth_letter + ".txt", 'a') as output_file:
                        length = len(emailPaswd)
                        #  Iterate through each index of the list and write it to the file
                        for index in range(length):
                            if index != length-1:
                                output_file.write(emailPaswd[index] + ":")
                            else:  # Don't add a ':' at the end of the line
                                output_file.write(emailPaswd[index])
                        output_file.write("\n")
                        return 1
                elif folder_depth == 3:  # Check to see if the fourth letter is an outlier EX) exa!mple@example.com
                    if not os.path.isdir(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/0UTLIERS"):
                        os.makedirs(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/0UTLIERS")
                    #  Make the 0UTLIERS file
                    with open(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/0UTLIERS/0utliers.txt", 'a') as output_file:
                        #  Get the new line from the emailPasswd list
                        length = len(emailPaswd)
                        new_line = ""
                        #  Iterate through each index and add it to new_line
                        for index in range(length):
                            if index != length - 1:
                                new_line += emailPaswd[index] + ":"
                            else:
                                new_line += emailPaswd[index]

                        if check_duplicate(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/0UTLIERS/0utliers.txt", new_line):
                            output_file.write(new_line + "\n")
                            return 1
                return 0
            else:  # The file exists
                if folder_depth == 4:  # The file does exist in the third dir but there is 4 valid chars
                    #  Get the new line from the emailPasswd list
                    length = len(emailPaswd)
                    new_line = ""
                    #  Iterate through each index and add it to new_line
                    for index in range(length):
                        if index != length - 1:
                            new_line += emailPaswd[index] + ":"
                        else:
                            new_line += emailPaswd[index]

                    if check_duplicate(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/" + fourth_letter + ".txt", new_line):
                        with open(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/" + fourth_letter + ".txt", 'a') as output_file:
                            output_file.write(new_line + "\n")
                        return 1
                    return 0
                elif folder_depth == 3:  # The file does exist in the third dir but there is only 3 valid chars
                    #  Check to see if you need to make the 0UTLIERS dir
                    if not os.path.isdir(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/0UTLIERS"):
                        os.makedirs(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/0UTLIERS")

                    #  Get the new line from the emailPasswd list
                    length = len(emailPaswd)
                    new_line = ""
                    #  Iterate through each index and add it to new_line
                    for index in range(length):
                        if index != length - 1:
                            new_line += emailPaswd[index] + ":"
                        else:
                            new_line += emailPaswd[index]

                    #  Check for duplicates and then write to the file
                    if check_duplicate(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/0UTLIERS/0utliers.txt", new_line):
                        #  Append the 0UTLIERS file
                        with open(path + "/data/" + first_letter + "/" + second_letter + "/" + third_letter + "/0UTLIERS/0utliers.txt", 'a') as output_file:
                            output_file.write(new_line + "\n")
                        return 1
                    return 0

        # NOT a valid email address or the username is NOT >= 4; or there is more than one '@' in the username
        else:
            if not os.path.isdir(path + "/data/NOTVALID"):
                os.makedirs(path + "/data/NOTVALID/")
                with open(path + "/data/NOTVALID/FAILED_TEST.txt", 'a') as fp:
                    length = len(emailPaswd)
                    #  Iterate through each index of the list and write it to the file
                    for index in range(length):
                        if index != length - 1:
                            fp.write(emailPaswd[index] + ":")
                        else:  # Don't add a ':' at the end of the line
                            fp.write(emailPaswd[index])
                    fp.write("\n")
                return 1
            else:  # The directory already exists
                if line != "":
                    #  Get the new line from the emailPasswd list
                    length = len(emailPaswd)
                    new_line = ""
                    #  Iterate through each index and add it to new_line
                    for index in range(length):
                        if index != length - 1:
                            new_line += emailPaswd[index] + ":"
                        else:
                            new_line += emailPaswd[index]

                    if check_duplicate(path + "/data/NOTVALID/FAILED_TEST.txt", new_line):
                        #  Open the file; check if it's a duplicate and write to the file
                        with open(path + "/data/NOTVALID/FAILED_TEST.txt", 'a') as fp:
                            fp.write(new_line + "\n")
                        return 1
            return 0
    except OSError:
        raise
    return 0

def handle_args() -> argparse.Namespace:
    """
    Function to enable users to import databases from external drives
    Contributing Author: https://github.com/ZacEllis
    :return: args
    """
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input_dir", default="PutYourDataBasesHere", help="Specify alternate input location")
    parser.add_argument("-e", "--export_dir", default=os.getcwd(), help="Specify alternative location to store your BaseQuery DB")
    parser.add_argument("file", help="File to index")
    args = parser.parse_args()

    if os.path.isdir(args.input_dir) == False: # Ensure input directory exists
        print(RED + "[!]" + NC + " Directory '" + args.input_dir + "' not found")
        exit(-1)

    file_path = os.path.join(args.input_dir, args.file)
    if os.path.exists(file_path) == False: # Ensure input file exists
        print(RED + "[!]" + NC + " File '" + args.file + "' not found in import location '" + args.input_dir + "'")
        exit(-1)

    unhandled_extensions = ["sql","csv","json","xlsx"]
    if "." in args.file:
        if args.file.split(".")[-1] in unhandled_extensions:
            print(YELLOW + "[!]" + NC + " File type '" + args.file.split(".")[-1] + "' currently unsupported (" + args.file + ")")
            exit(-1)

    return args


if __name__ == '__main__':
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

    #  Grab any user passed arguments
    args = handle_args()
    #  combine the passed import dir with file name
    file_path = os.path.join(args.input_dir, args.file)
    #  Grab the export path
    export_path = args.export_dir

    start_time = time.time()
    total_lines = 0  # The amount of lines that are not white-space
    written_lines = 0  # The amount of lines written

    print(GREEN + "[+]" + NC + " Opening file " + GREEN + args.file + NC)
    with open(file_path, 'r') as fp:
        try:
            for line in fp:
                #  For every 10,000th line print an update to the user
                if total_lines % 10000 == 0 and total_lines != 0:
                    print(GREEN + "[+]" + NC + " Processing line number: " + str(total_lines) + "\nLine: " + line)
                if line.strip() != "":
                    written_lines += place_data(line.strip(), export_path)
                    total_lines += 1
        except Exception as e:
            print(RED + "Exception: " + str(e) + NC)
    stop_time = time.time()

    # Useful metrics
    out_total_time    = GREEN + "[+]" + NC + " Total time: "    + str(("%.2f" % (stop_time - start_time)) + " seconds")
    out_total_lines   = GREEN + "[+]" + NC + " Total lines: "   + str(("%.2f" % total_lines))
    out_written_lines = GREEN + "[+]" + NC + " Written lines: " + str(("%.2f" % written_lines))

    #  Output to Stdout
    print("\n" + out_total_time + "\n" + out_total_lines + "\n" + out_written_lines)

    # Log times
    with open(os.path.join(os.getcwd(), "Logs/ActivityLogs.log"), 'a') as log:
            log.write("[+] Total time: " + str(("%.2f" % (stop_time - start_time)) + " seconds") + "\n")
            log.write("[+] Total lines: " + str(("%.2f" % total_lines)) + "\n")
            log.write("[+] Written lines: " + str(("%.2f" % written_lines)) + "\n")
