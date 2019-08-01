#!/usr/bin/python

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
print(current_dir[:current_dir.rfind(path.sep + "modules")])
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep + "modules")])
from lib.objects.local_string_generator import StringGenerator
import lib.helpers.constants as constants
sys.path.pop(0)

import json
import random

#require 'faker'

class FilenameGenerator (StringEncoder):
    file_name = ''
    extension = ''

    def __init__(self):
        super
        self.module_name = 'Random Filename Generator'
        self.file_name = ''
        self.extension = ''


    def encode_all(self):
        file_name = self.file_name
        extension = self.extension
        leaked_filenames = []

        if file_name == '':
            file_name = None
            leaked_filenames = random.choice(['top_secret_information', 'secrets', 'hush_hush', 'private_stuff', 'restricted', 'classified', 'confidential'])

        if extension == '':
            extension = None

        if self.extension == 'no_extension':
            extension = ''

        for x in range(0, 15):
            leaked_filenames = leaked_filenames.append(file_name+"."+extension)

        output = leaked_filenames[0]

        print(output)

    def process_options(opts):
        super
        for opt, arg in opts:
            if opt in ('---file_name'):
                self.file_name = arg
            elif opt in ('--extension'):
                self.extension = arg

    def get_options_array():
        super
        ['--file_name','--extension']

    def encoding_print_string(self):
        string = ''
        if self.file_name == None and self.extension == None:
            string = 'No args'
        else:
            if len(self.file_name) > 0 and len(self.extension) > 0:
                string += 'file_name: ' + str(self.file_name) + 'extension: ' + str(self.extension)
            elif len(self.file_name) > 0:
                string += 'file_name: ' + str(self.file_name)
            else:
                string += 'extension: ' + str(self.extension)
        return string

if __name__ == "__main__":
    FilenameGenerator.process_options()
