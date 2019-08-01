#!/usr/bin/python

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
print(current_dir[:current_dir.rfind(path.sep + "modules")])
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep + "modules")])
from lib.objects.local_string_generator import StringGenerator
import lib.helpers.constants as constants
sys.path.pop(0)

import random

class WelcomeMessageGenerator (StringGenerator):
    def initialize():
        super
        self.module_name = 'Welcome Message Generator'

    def generate():
        messages = ['Welcome to the server!', 'Greetings! Welcome to the server.', "G'day mate!"]
        print(random.choice(messages))

if __name__ == "__main__":
    WelcomeMessageGenerator.generate()