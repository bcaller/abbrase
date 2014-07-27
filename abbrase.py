"""abbrase.py: generates passwords by abbreviating passphrases"""

__author__ =    'Ben Caller (bcaller)'
__copyright__ = 'Copyright 2014, Benjamin Caller'
__credits__ =   ['Ryan Hitchman (rmmh)']
__license__ =   'MIT'

import json
import random
import math


def import_data():
    with open('unigrams.json') as unigrams:
        return json.load(unigrams)


data = import_data()
rand = random.SystemRandom()


def random_sample_with_replacement(seq, num):
    sequence = list(seq)
    return (sequence[rand.randrange(len(sequence))] for _ in range(num))


def phrase(words, pos):
    for prefix, i in zip(words, pos):
        if data[prefix][i]:
            yield prefix + random.choice(data[prefix][i])
        else:
            choices = [w for part in data[prefix] for w in part]
            if choices:
                yield random.choice(choices)
            else:
                yield prefix + '??'


def abbrase(abbrs=None, parts_of_speech=None, num=None, all_prefixes=set()):
    if parts_of_speech is None:
        zeroes = 2
        if not abbrs is None:  # default to: adj* noun verb adj* noun
            zeroes = len(abbrs) - 3
        elif not num is None:
            zeroes = num - 3
        parts_of_speech = [0] * math.floor(zeroes / 2) + [1, 2] + [0] * math.ceil(zeroes / 2) + [1]
    if abbrs is None:
        if len(all_prefixes) == 0:
            all_prefixes.update(set(data.keys()))

        abbrs = random_sample_with_replacement(all_prefixes, len(parts_of_speech))
    return ' '.join(phrase(abbrs, parts_of_speech))


def abbreviate(passphrase):
    return ''.join((w[:3] for w in passphrase.split(" ")))


def printable(passphrase):
    return abbreviate(passphrase) + ' | ' + passphrase

if __name__ == '__main__':
    for i in range(5):
        print(printable(abbrase(num=5)))

    print('\n')

    for i in range(2):
        print(printable(abbrase(num=6)))
    print('\n')
    for i in range(2):
        print(printable(abbrase(num=7)))