#!/usr/bin/env python3.7
try:
    import string
    import random
except Exception as e:
    print(e)
    exit(1)

"""
Author Github:   https://github.com/g666gle      
Author Twitter:  https://twitter.com/g666g1e
Date:            12/1/2019
Description:     This file when run by itself creates a randomly generated combo-list in the format email:password
                 The username for the email address can vary in size from 2 characters long to 10 characters long.
                 The password can vary in length from 2 characters long to 12 characters long. The randomly generated
                 strings are made using only alphanumeric characters [a-z][A-Z][0-9]
Usage:           python3 MakeFakeDB.py
Version:	     2.0.0
Python Version:  3.7.1
"""

AMT_LINES = 1000000


def random_string_generator(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


if __name__ == '__main__':
    with open("Fake_1Million_DB.txt", 'a') as fp:
        print("Please wait this could take a while...")
        for _ in range(AMT_LINES):
            uname = random_string_generator(random.randint(2, 10))
            pw = random_string_generator(random.randint(2, 12))
            fp.write(uname.lower() + "@fake.com:" + pw.lower() + "\n")
