#!/usr/bin/python

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
print(current_dir[:current_dir.rfind(path.sep + "modules")])
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep + "modules")])
from lib.objects.local_string_generator import StringGenerator
import lib.helpers.constants as constants
sys.path.pop(0)

from copy import copy
import random
import secrets
import string
import base64

class StrongPasswordGenerator(StringGenerator):
    def __init__(self):
        super
        self.module_name = 'Random Strong Password Generator'

    def generate():
        password = base64.b64encode(bytes(random._urandom(15)),).decode('ascii')
        password = password.replace('/','')
        password = password.replace('+','')
        print(password.replace('=',''))

if __name__ == "__main__":
    StrongPasswordGenerator.generate()