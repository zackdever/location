#!/usr/bin/env python

from testapi import test as api
from testauth import test as auth
from testmodels import test as models

def test():
    api()
    auth()
    models()

if __name__ == '__main__':
    test()
