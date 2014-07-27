"""merge_dict.py: merges the output json files of unigrams.py into one json file"""

__author__ = 'Ben Caller (bcaller)'
__copyright__ = 'Copyright 2014, Benjamin Caller'
__license__ = 'MIT'

import json


def merge():
    letters = set()

    with open("./data/prefixes.txt") as prefListFile:
        for pref in prefListFile.readline().split(','):
            letters.add(pref[0])

    words = dict()
    for l in letters:
        with open('./data/' + l + '.json') as file:
            partial_dictionary = json.load(file)
            words.update(partial_dictionary)

    print('Writing to unigrams.json')
    with open('unigrams.json', 'w') as outfile:
        json.dump(words, outfile)


if __name__ == '__main__':
    merge()