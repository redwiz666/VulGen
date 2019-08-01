#!/usr/bin/python

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
print(current_dir[:current_dir.rfind(path.sep + "modules")])
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep + "modules")])
from lib.objects.local_string_generator import StringGenerator
import lib.helpers.constants as constants
sys.path.pop(0)

import getopt
from copy import copy

class CustomPasswordGenerator(StringGenerator):

    list_name = ''
    def __init__():
        super
        self.module_name = 'Custom List Password Generator'
        self.list_name = ''

    def generate():
        try:
            opts, remainder = getopt.gnu_getopt(sys.argv[1:], ' ', CustomPasswordGenerator.get_options_array())
        except getopt.GetoptError as err:
            print (str(err))
            sys.exit(1)

        CustomPasswordGenerator.process_options(opts)

        with open(constants.PASSWORDLISTS_DIR +"/" + CustomPasswordGenerator.list_name) as f:
            tmp = f.read().splitlines()
            t = copy(tmp)
        for word in t:
            if word[0] == "#":
                tmp.remove(word)
        print(tmp)

    def get_options_array():
        super 
        return ['list_name=',]

    def process_options(opts):
        super
        for opt, arg in opts:
            if opt in ('--list_name'):
                CustomPasswordGenerator.list_name = arg

    def encoding_print_string():
        print('list_name: ' + str(list_name))

if __name__ == "__main__":
    CustomPasswordGenerator.generate()