#! /usr/bin/env python
import sys
from flask.ext.script import Manager, Server
from ann import app


def run_server(manager):
    manager.add_command("run", Server(port=5000))
    manager.run()

def main():
    manager = Manager(app)
    run_server(manager)

if __name__ == '__main__':
    sys.exit(main())
