"""test_prefix.py: 2 unit tests for the finish method of Prefix"""

__author__ = 'Ben Caller (bcaller)'
__copyright__ = 'Copyright 2014, Benjamin Caller'
__license__ = 'MIT'

from unittest import TestCase
from Prefix import Prefix


class TestPrefix(TestCase):
    def test___group_verbs(self):

        tests = [
            (['catch', 'catches', 'catching'], ['catching']),
            (['study', 'studies', 'studying', 'studied'], ['studied']),
            (['kill', 'kills', 'killed', 'killing'], ['kills']),
            (['kiss', 'kisses', 'kissed', 'kissing'], ['kisses']),
            (['buy', 'buying', 'buys'], ['buying']),
            (['bite', 'bites', 'bit', 'biting'], ['biting']),
            (['hate', 'hates', 'hated', 'hating'], ['hates']),
            (['hate', 'hates', 'hating'], ['hating']),
            (['muse', 'mused', 'musing', 'muses'], ['muses']),
            (['muse', 'musing', 'muses'], ['musing']),
            (['muse', 'mused', 'muses', 'musing', 'muss', 'mussed', 'mussing'],
             ['muse', 'mused', 'muses', 'musing', 'muss', 'mussed', 'mussing']),
            (['cuss', 'cusses', 'cussin', 'cus', 'cuse', 'cused', 'cussing', 'cusing', 'cussed'],
             ['cusses', 'cussin', 'cuse', 'cused']),
            (['seeing', 'sees', 'see'], ['seeing']),
            (['writing', 'write', 'writ', 'wring', 'written', 'writen', 'wringing', 'writeing', 'wrings', 'writes', 'writt', 'writting'],
             ['writing', 'writen', 'written', 'wringing', 'writt', 'writting'])
        ]
        for t in tests:
            for pre in [0, 3]:
                p = Prefix([{}, {}, {x[pre:]: 1 for x in t[0]}])
                p.finish(10)
                self.assertEqual(set(p.VERB.keys()), {x[pre:] for x in t[1]})

    def test___depluralise_nouns(self):
        tests = [
            (['cake', 'cakes'], ['cake']),
            (['kiss', 'kisses'], ['kiss']),
            (['countries', 'country'], ['country']),
            (['monkeys', 'monkey'], ['monkey']),
            (['battery', 'batteries'], ['battery']),
            (['battery', 'batterys', 'batteries'], ['battery']),
            (['battery', 'batterys'], ['battery'])
        ]
        for t in tests:
            for pre in [0, 3]:
                p = Prefix([{}, {x[pre:]: 1 for x in t[0]}, {}])
                p.finish(10)
                self.assertEqual(set(p.NOUN.keys()), {x[pre:] for x in t[1]})