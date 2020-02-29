#!/usr/bin/env python3.7
try:
    from pyhunter import PyHunter
    import argparse
    import yaml
    import os
    import pprint
    import json
except Exception as e:
    print(e)
    exit(1)

"""
Author Github:   https://github.com/g666gle
Author Twitter:  https://twitter.com/g666g1e
Date:            12/3/2019
Description:     
Version:	     1.5.0
Python Version:  3.7.1
"""

GREEN = '\033[0;32m'
NC = '\033[0m'  # No Color


def domain_search(args, hunter):
    """

    :param args:
    :param hunter:
    :return:
    """
    _domain = None
    _company = None
    _limit = None
    _offset = None
    _emails_type = None
    if args.domain != "None":
        _domain = args.domain
    if args.company != "None":
        _company = args.company
    if args.limit != "None":
        _limit = args.limit
    if args.offset != "None":
        _offset = args.offset
    if args.emails_type != "None":
        _emails_type = args.emails_type
    data = hunter.domain_search(domain=_domain, company=_company, limit=_limit, offset=_offset, emails_type=_emails_type)
    if args.out_to_file == "True":
        if _domain is not None:
            with open(str(os.getcwd()) + "/OutputFiles/" + _domain + ".txt", 'a') as fp:
                print(GREEN + "[!] Results are being outputed to " + str(os.getcwd()) + "/OutputFiles/" + _domain + ".txt" + NC)
                fp.write(json.dumps(data))
        else:
            with open(str(os.getcwd()) + "/OutputFiles/" + _company + ".txt", 'a') as fp:
                print(GREEN + "[!] Results are being outputed to " + str(os.getcwd()) + "/OutputFiles/" + _company + ".txt" + NC)
                fp.write(json.dumps(data))
    else:
        print("\n")
        pprint.pprint(data)
        print("\n")


def email_finder(args, hunter):
    _domain = None
    _company = None
    _first_name = None
    _last_name = None
    _full_name = None
    if args.domain != "None":
        _domain = args.domain
    if args.company != "None":
        _company = args.company
    if args.first_name != "None":
        _first_name = args.first_name
    if args.last_name != "None":
        _last_name = args.last_name
    if args.full_name != "None":
        _full_name = args.full_name
    data = hunter.email_finder(domain=_domain, company=_company, first_name=_first_name, last_name=_last_name, full_name=_full_name)
    print("\n")
    pprint.pprint(data)
    print("\n")


def email_verifier(args, hunter):
    _email = args.email
    data = hunter.email_verifier(email=_email)
    print("\n")
    pprint.pprint(data)
    print("\n")


def email_count(args, hunter):
    _domain = None
    _company = None
    if args.domain != "None":
        _domain = args.domain
    if args.company != "None":
        _company = args.company
    data = hunter.email_count(domain=_domain, company=_company)
    print("\n")
    pprint.pprint(data)
    print("\n")


def account_information(hunter):
    data = hunter.account_information()
    print("\n")
    pprint.pprint(data)
    print("\n")


def make_call(args, hunter):
    """

    :param args:
    :param hunter:
    :return:
    """
    if args.domain_search == 'True':
        domain_search(args, hunter)
    elif args.email_finder == 'True':
        email_finder(args, hunter)
    elif args.email_verifier == 'True':
        email_verifier(args, hunter)
    elif args.email_count == 'True':
        email_count(args, hunter)
    elif args.account_information == 'True':
        account_information(hunter)


def handle_args():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    #  Different types of searches
    parser.add_argument("-ds", "--domain_search", help="Returns all the email addresses found using one given domain name, with sources")
    parser.add_argument("-ef", "--email_finder", help="Guesses the most likely email of a person using his/her first name, last name and a domain name")
    parser.add_argument("-ev", "--email_verifier", help="Checks the deliverability of a given email address, verifies if it has been found in our database, and returns their sources")
    parser.add_argument("-ec", "--email_count", help="You can check how many email addresses Hunter has for a given domain")
    parser.add_argument("-ai", "--account_information", help="You can check your account information")

    #  All the possible options for the above searches
    parser.add_argument("--domain", help="The domain of the company where the person works. Must be defined if company is not.")
    parser.add_argument("--company", help="The name of the company where the person works. Must be defined if domain is not.")
    parser.add_argument("--limit", help="Specify alternate input location")
    parser.add_argument("--offset", help="Specify alternate input location")
    parser.add_argument("--emails_type", help="The type of emails to give back. Can be one of 'personal' or 'generic'.")
    parser.add_argument("--first_name", help="The first name of the person. Must be defined if full_name is not.")
    parser.add_argument("--last_name", help="The last name of the person. Must be defined if full_name is not.")
    parser.add_argument("--full_name", help="The full name of the person. Must be defined if first_name AND last_name are not.")
    parser.add_argument("--email", help="The email address to check.")
    parser.add_argument("--out_to_file", help="This should be set to True if you want the results outputed to a file")
    return parser.parse_args()


if __name__ == '__main__':
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

    HUNTER_IO_API_KEY = ''
    args = handle_args()

    #  Checks to make sure your in the BaseQuery directory
    if os.getcwd().split('/')[-1] == 'BaseQuery':
        #  Checks to see if the file exists
        if os.path.isfile("./Logs/api_keys.yml"):
            #  Opens the yml file and
            with open("./Logs/api_keys.yml", 'r') as stream:
                try:
                    # No that's not a real API key, just an example
                    # {'apikeys': {'hunter': {'key': 'ghsdjfsd678dsfr7dfv'}}}
                    dict = yaml.safe_load(stream)
                    for apikeys in dict.values():
                        for hunter in apikeys.values():
                            for key in hunter.values():
                                HUNTER_IO_API_KEY = key
                except yaml.YAMLError as exc:
                    print(exc)
    if HUNTER_IO_API_KEY is not None:
        hunter = PyHunter(HUNTER_IO_API_KEY)
        make_call(args, hunter)
    else:
        print()
        print(RED + "[!]" + NC + " Hunter.io API key missing!")
        print(RED + "Make sure you added your apikey in Logs/api_keys.yml If you don't have one go to hunter.io to get one for free!" + NC)
