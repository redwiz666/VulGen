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

class MediumPasswordGenerator (StringGenerator):
    
    def __init__(self):
        super
        self.module_name = 'Random Medium Password Generator'

    def generate():
        with open(constants.WORDLISTS_DIR +"/nouns") as f:
            nouns = f.read().splitlines()
        with open(constants.WORDLISTS_DIR +"/adjectives") as f:
            adjectives = f.read().splitlines()
        with open(constants.WORDLISTS_DIR +"/top_usa_male_names") as f:
            male_names = f.read().splitlines()
        with open(constants.WORDLISTS_DIR +"/top_usa_female_names") as f:
            female_names = f.read().splitlines()

        all_words = adjectives + nouns + male_names + female_names

        tmp = copy(all_words)
        for word in tmp:
            if len(word) != 6:
                all_words.remove(word)
        
        random.shuffle(all_words)
        word = all_words[0]


        number = str(random.randint(1,4))
        print(word+number)

if __name__ == "__main__":
    MediumPasswordGenerator.generate()