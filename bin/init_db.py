#! /usr/bin/env python

import os
import sys
from sqlite3 import OperationalError
os.path.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ann


class Command:
    def __init__(self):
        pass
     
    def account(self):
        try:
            ann.app.acc.create_table()
        except OperationalError as e:
            print str(e)

    def message(self):
        try:
            ann.app.msg.create_table()
        except OperationalError as e:
            print str(e)

    def all(self):
        try:
            ann.app.acc.create_table()
            ann.app.msg.create_table()
        except OperationalError as e:
            print str(e)

def main():
    """
    Create tables
    """
    command = Command()
    
    if hasattr(command, sys.argv[1].lstrip('-')):
        getattr(command,sys.argv[1].lstrip('-'))()
    else:
        print "Unsupport command: {}".format(sys.argv[1])

if __name__ == '__main__':
    sys.exit(main())






