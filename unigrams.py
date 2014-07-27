"""unigrams.py: process the [a-z].gz files to [a-z].json with common words grouped by part of speech"""

__author__ = 'Ben Caller (bcaller)'
__copyright__ = 'Copyright 2014, Benjamin Caller'
__credits__ = ['Ryan Hitchman (rmmh)']
__license__ = 'MIT'

import json
from Prefix import Prefix
from merge_dict import merge
import gzip
import re

hasPartOfSpeech = re.compile('^([A-Za-z][a-z]+)_(ADJ|NOUN|VERB)')
pos = ['ADJ', 'NOUN', 'VERB']
prefixes = set()
with open("./data/prefixes.txt") as prefListFile:
    for pref in prefListFile.readline().split(','):
        prefixes.add(pref)

for letter in {pref[0] for pref in prefixes}:
    currentLetterPrefixes = {p for p in prefixes if p[0] == letter}
    unigram = {p: Prefix() for p in currentLetterPrefixes}
    
    print(currentLetterPrefixes)
    
    linesRead = 0
    for bline in gzip.GzipFile("./data/" + letter + '.gz'):

        linesRead += 1
        if linesRead % 3e6 == 0:
            print(linesRead / 1e6, sep=" " if linesRead % 2e6 == 0 else "\n", flush=True)  # number of lines read (millions)

        line = bline.decode('utf-8')
        prefix = line[:3]
        if prefix in currentLetterPrefixes:
            parts = line.split()
            if int(parts[1]) > 1950:  # ignore older books
                hasPos = hasPartOfSpeech.match(parts[0])
                if hasPos:  # annotated with part of speech
                    suffix = hasPos.group(1).lower()[3:]
                    count = int(parts[3])
                    if len(suffix) < 10 and count > 100:  # nice popular words please
                        posIndex = pos.index(hasPos.group(2))
                        unigram[prefix].put(suffix, posIndex, count)

    for p in currentLetterPrefixes:
        print('Ready to aggregate for letter {}'.format(p), flush=True)
        # print(unigram[p].parts)
        unigram[p].finish()
    
    with open('./data/' + letter + '.json', 'w') as outfile:
        json.dump({pre: unigram[pre].data() for pre in unigram}, outfile)

    print('finished ' + letter)

print('yeah baby!')
merge()  # now make the unigrams.json