#!/usr/bin/python

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
print(current_dir[:current_dir.rfind(path.sep + "modules")])
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep + "modules")])
from lib.objects.local_string_generator import StringGenerator
import lib.helpers.constants as constants
sys.path.pop(0)

import re, getopt, string
import random

class LineGenerator (StringGenerator):
  
    linelist = []

    def __init__(self):
        super
        self.linelist = []
        self.module_name = 'Random Word Generator'

    def get_options_array():
        super 
        return ['linelist=']


    def process_options(opts):
        super
        for opt, arg in opts:
            if opt in ('--linelist'):
                LineGenerator.linelist = arg


    def generate():
        try:
            opts, remainder = getopt.gnu_getopt(sys.argv[1:], '', LineGenerator.get_options_array())
        except getopt.GetoptError as err:
            print (str(err))
            sys.exit(1)

        LineGenerator.process_options(opts)

        # read all the lines, and select one at random
        with open(constants.LINELISTS_DIR +"/" + LineGenerator.linelist) as f:
            line = f.read().splitlines()
        line = line[random.randint(0,len(line)-1)]
        # strip out everything except alphanumeric and basic punctuation (no ' or ")
        line.translate(str.maketrans('', '', string.punctuation))
        print(line)

if __name__ == "__main__":
    LineGenerator.generate()
