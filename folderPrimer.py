#!/usr/bin/env python3.7
try:
    import os
    import sys
    import time
except Exception as e:
    print(e)
    exit(1)

"""
Author Github:   https://github.com/g666gle      
Author Twitter:  https://twitter.com/g666g1e
Date:            12/1/2019
Description:     This file creates a triple nested [A-Z] and [0-9] directories so the data from the databases are easily 
                 accessible. The reason to do this before instead of while pysort.py is placing all the files is due to 
                 the fact that creating directories is slightly time consuming and by creating them all at once instead 
                 of on the fly. We can expect to see a small efficiency improvement. Also.... organization 
Usage:           python3 folderPrimer.py
Usage:           python3 folderPrimer.py /full/path/to/dir/to/prime
Version:	     2.0.0
Python Version:  3.7.1
"""

path = os.getcwd()


def folder_spam():
    """
    This function creates all the nested files needed to store the data. [A-Z][0-9]
    :return: N/A
    """
    first_nest =  ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    second_nest = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    third_nest =  ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    for char in first_nest:  # Creating the first nesting of the folders
        if not os.path.isdir(path + "/data/" + char.strip()):
            os.makedirs(path + "/data/" + char.strip())
    for char in first_nest:  # Creating the second nesting of the folders
        for char2 in second_nest:
            if not os.path.isdir(path + "/data/" + char.strip() + "/" + char2.strip()):
                os.makedirs(path + "/data/" + char.strip() + "/" + char2.strip())
    for char in first_nest:  # Creating the third nesting of the folders
        for char2 in second_nest:
            for char3 in third_nest:
                if not os.path.isdir(path + "/data/" + char.strip() + "/" + char2.strip() + "/" + char3.strip()):
                    os.makedirs(path + "/data/" + char.strip() + "/" + char2.strip() + "/" + char3.strip())


def folder_spam_remote(full_path_to_dir):
    """
    This function creates all the nested files needed to store the data. [A-Z][0-9] in a directory besides the default
    :return: N/A
    """
    first_nest =  ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    second_nest = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    third_nest =  ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    for char in first_nest:  # Creating the first nesting of the folders
        if not os.path.isdir(full_path_to_dir + "/" + char.strip()):
            os.makedirs(full_path_to_dir + "/" + char.strip())
    for char in first_nest:  # Creating the second nesting of the folders
        for char2 in second_nest:
            if not os.path.isdir(full_path_to_dir + "/" + char.strip() + "/" + char2.strip()):
                os.makedirs(full_path_to_dir + "/" + char.strip() + "/" + char2.strip())
    for char in first_nest:  # Creating the third nesting of the folders
        for char2 in second_nest:
            for char3 in third_nest:
                if not os.path.isdir(full_path_to_dir + "/" + char.strip() + "/" + char2.strip() + "/" + char3.strip()):
                    os.makedirs(full_path_to_dir + "/" + char.strip() + "/" + char2.strip() + "/" + char3.strip())


if __name__ == '__main__':
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

    argv = sys.argv
    # A external dir is given to prime
    if len(argv) == 2:
        if os.path.isdir(argv[1]):
            print()
            print(GREEN + "[+]" + NC + " Priming the data directory")
            start_time = time.time()
            folder_spam_remote(argv[1])
            end_time = time.time()
            print(GREEN + "[+]" + NC + " Data directory finished being primed!")
            print(YELLOW + "[!]" + NC + " Action took " + str(int(end_time - start_time)) + " seconds")
            print()
        else:
            print(RED + "[!]" + NC + " ERROR: directory given does not exist!")
    # No args passed. Prime the default dir
    elif len(argv) == 1:
        if os.path.isdir(path + "/data"):
            print()
            print(GREEN + "[+]" + NC + " Priming the data directory")
            start_time = time.time()
            folder_spam()
            end_time = time.time()
            print(GREEN + "[+]" + NC + " Data directory finished being primed!")
            print(YELLOW + "[!]" + NC + " Action took " + str(int(end_time - start_time)) + " seconds")
            print()
        else:
            print(RED + "[!]" + NC + " ERROR: directory given does not exist!")
    else:
        print(RED + "[+]" + NC + " Wrong number of arguments passed!")
