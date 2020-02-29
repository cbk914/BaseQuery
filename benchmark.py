#!/usr/bin/env python3.7

try:
    import shutil
    from pysort import *
    from folderPrimer import *
except Exception as e:
    print(e)
    exit(1)

"""
Author Github:   https://github.com/g666gle      
Author Twitter:  https://twitter.com/g666g1e
Date:            12/1/2019
Description:     This file is used by run.sh to calculate the amount of time it will take the current hardware to process
                 the user specified amount of lines. This is important because each user has different hardware. Import
                 mainly relies on the type of CPU and how many cores it has. On an Intel i7-7700 processor and 16GB of
                 RAM you can expect results of around 10000 lines per second while your laptop is plugged in and 5000
                 lines per second while your laptop is not plugged in. The reason this is a worst case scenario is 
                 because the fake combo-list file I generated has cryptographically random usernames and passwords. In 
                 english this means all of the usernames and passwords are very different and this means BaseQuery has 
                 to traverse many more directories than normal. In a normal data-leak we see a normal distribution 
                 around, roughly, 8 characters.
                  
Usage:           python3 benchmark.py <number of lines>
Usage:           python3 benchmark.py 1000000
Version:	     2.0.0
Python Version:  3.7.1
"""

if __name__ == '__main__':
    #  the arguments passed in
    args = sys.argv
    path = os.getcwd()
    written_lines = 0
    # The amount of lines written in 30 Second
    total_lines = 0

    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

    AMT_SECONDS = 30
    FILE_NAME = "Fake_1Million_DB.txt"
    num_lines = sum(1 for line in open(path + "/Logs/temp_benchmark_DB/" + FILE_NAME, 'r'))

    #  Check to see if the arguments are correct
    if len(args) >= 2:
        #  Grab the users imputed amount of lines
        amt_lines = args[1]
        if not os.path.isdir(path + "/Logs/"):
            os.makedirs(path + "/Logs/")
        if not os.path.isdir(path + "/Logs/temp_benchmark_DB/"):
            os.makedirs(path + "/Logs/temp_benchmark_DB/")
        if not os.path.isdir(path + "/Logs/temp_benchmark_DB/data"):
            os.makedirs(path + "/Logs/temp_benchmark_DB/data")

        if os.path.isfile(path + "/Logs/temp_benchmark_DB/" + FILE_NAME):
            os.system("python3.7 folderPrimer.py " + path + "/Logs/temp_benchmark_DB/data")
            #  Open the fake DB and go through each file
            with open(path + "/Logs/temp_benchmark_DB/" + FILE_NAME, 'r') as fp:
                try:
                    start_time = time.time()
                    for line in fp:
                        #  For every 10,000th line print an update to the user
                        if total_lines % 10000 == 0 and total_lines != 0:
                            print(GREEN + "[+]" + NC + " Processing line number: " + str(total_lines))
                        if (time.time() - start_time) <= AMT_SECONDS:
                            if line.strip() != "":
                                written_lines += place_data(line.strip(), path + "/Logs/temp_benchmark_DB/")
                                total_lines += 1
                        else:
                            break
                except Exception as e:
                    print(RED + "Exception: " + str(e) + NC)
            stop_time = time.time()
        else:
            print("ERROR: ./Logs/temp_benchmark_DB/" + FILE_NAME + " not found! Did you delete it?")
            exit(1)
        print()
        print(GREEN + "[!]" + NC + " Removing the temporary benchmark data!")

        #  Remove the temporary BQ database
        folder = path + "/Logs/temp_benchmark_DB/data"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        if total_lines != 0:
            #  The seconds is ( ( 30 * ( user imputed lines ) ) / ( amount of lines processed in 2 seconds ) )
            secs = (AMT_SECONDS * int(amt_lines)) / int(total_lines)
            mins = secs / 60
            hours = mins / 60
            days = hours / 24
            years = days / 364
            os.system('cls' if os.name == 'nt' else 'clear')
            print(YELLOW + "[!]" + NC + " Your computer can process " + RED + str(round(total_lines / AMT_SECONDS, 2)) + NC + " lines per second!")
            print(YELLOW + "[!]" + NC + " Your computer processed " + str(total_lines) + " lines in " + str(AMT_SECONDS) + " seconds! The test file had a total of " + str(num_lines) + " lines!")
            print(YELLOW + "[!] Please note this is a WORST CASE SCENARIO! Expect slightly better results during import!" + NC)
            print(YELLOW + "[!] For the best results make sure your laptop is plugged into a power source!" + NC)
            print()
            print(GREEN + "[+]" + NC + " To import " + GREEN + amt_lines + NC + " lines")
            print(GREEN + "[+]" + NC + " You can expect an import time of around " + GREEN + "{}".format('%.2f' % secs) + NC + " seconds which is...")
            print("                                            " + GREEN + "{}".format('%.2f' % mins) + NC + " minutes which is...")
            print("                                            " + GREEN + "{}".format('%.2f' % hours) + NC + " hours which is...")
            print("                                            " + GREEN + "{}".format('%.2f' % days) + NC + " days which is...")
            print("                                            " + GREEN + "{}".format('%.2f' % years) + NC + " years!")
        else:
            print(RED + "ERROR [!] " + NC + "0 Lines were processed!")
    else:
        print(YELLOW + "[!]" + NC + " Invalid arguments provided")
