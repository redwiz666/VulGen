import lib.helpers.constants as constants
import sys

sys.dont_write_bytecode = True



class blacklist:
    def __init__(self):
        with open(constants.BLACKLISTED_WORDS_FILE) as file:
            self.blacklisted_words = [line.strip() for line in file]

    def is_blacklisted(word):
        return blacklisted_words.contains(word)