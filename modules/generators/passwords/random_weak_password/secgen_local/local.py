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
from random import shuffle

class WeakPasswordGenerator(StringGenerator):
  
    def __init__(self):
        super
        self.module_name = 'Random Weak Password Generator'
        words = []

    def generate():
        with open(constants.WORDLISTS_DIR +"/nouns") as f:
            nouns = f.read().splitlines()
        with open(constants.WORDLISTS_DIR +"/top_usa_male_names") as f:
            male_names = f.read().splitlines()
        with open(constants.WORDLISTS_DIR +"/top_usa_female_names") as f:
            female_names = f.read().splitlines()

        all_words = nouns + male_names + female_names

        # only keep words 3-5 characters
        org_list = copy(all_words)
        for word in org_list:
            if len(word) < 3 or len(word) > 5:
                all_words.remove(word)
        shuffle(all_words)
        print(all_words)


if __name__ == "__main__":
    WeakPasswordGenerator.generate()