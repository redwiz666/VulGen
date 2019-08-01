#!/usr/bin/python

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
print(current_dir[:current_dir.rfind(path.sep + "modules")])
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep + "modules")])
from lib.objects.local_string_generator import StringGenerator
import lib.helpers.constants as constants
sys.path.pop(0)

class CommonPasswordGenerator (StringGenerator):
    def __init__(self):
        super
        self.module_name = 'Random Common Password Generator'

    def generate():
        with open(constants.WORDLISTS_DIR +"/10_million_password_list_top_100") as f:
            tmp = f.read().splitlines()
        print(tmp)


if __name__ == "__main__":
    CommonPasswordGenerator.generate()