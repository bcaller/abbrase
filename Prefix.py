"""Prefix.py: Prefix class for reading in unigram data"""

__author__ = 'Ben Caller (bcaller)'
__copyright__ = 'Copyright 2014, Benjamin Caller'
__license__ = 'MIT'

class Prefix:
    """List of dictionaries of {suffix: occurrence} for a particular prefix for reading unigram data"""
    def __init__(self, parts=None):
        if parts is None:
            self.parts = [{}, {}, {}]
        else:
            assert len(parts) == 3
            self.parts = parts
        self.ADJ, self.NOUN, self.VERB = self.parts[0], self.parts[1], self.parts[2]

    def put(self, suffix, pos_index, count):
        """Records a suffix in the dictionary for the part of speech and updates its count"""
        if suffix in self.parts[pos_index]:
            self.parts[pos_index][suffix] += count
        else:
            self.parts[pos_index][suffix] = count

    def get_word_counts(self, pos_index):
        """Tuples of (suffix, occurrences)"""
        words = self.parts[pos_index]
        return [
            (w, words[w])
            for w in sort_desc(words)
        ]

    def data(self):
        """Export as simple list of 3 dictionaries"""
        return [sort_desc(pos_words) for pos_words in self.parts]

    def __trim(self, num=6):
        for i in range(3):
            for (word, _) in self.get_word_counts(i)[num:]:
                del self.parts[i][word]

            word_counts = self.get_word_counts(i)
            for (word, count) in word_counts[2:]:
                if count < word_counts[0][1] / 11:
                    del self.parts[i][word]

    def __group_ed_verbs(self):
        verb_keys = top_few(self.VERB, 100)
        for verb in verb_keys:
            if len(verb) > 1 and verb[-2:] == 'ed':
                stem = verb[:-2]
                if stem + 'ing' in verb_keys:
                    if bool(stem + 's' in verb_keys) ^ bool(stem + 'es' in verb_keys):
                        combine(self.VERB, stem + 'ing', verb)  # ing to ed
                        if stem + 's' in verb_keys:
                            if stem in verb_keys:  # no suffix after verb stem -> put 'ed' on end temporarily
                                combine(self.VERB, stem, verb)
                            if len(stem) > 0 and not stem[-1] == 's':  # otherwise cannot be sure what is going on
                                combine(self.VERB, verb, stem + 's')
                        else:
                            if stem + 'e' in verb_keys and verb[-1]:  # no suffix after verb stem -> put 'd' on end
                                combine(self.VERB, stem + 'e', verb)
                            elif stem in verb_keys:
                                combine(self.VERB, stem, verb)
                            combine(self.VERB, verb, stem + 'es')
                elif len(stem) > 0 and stem[-1] == 'i' and not stem[:-1] + 'yed' in verb_keys:  # studied
                    y_stem = stem[:-1] + 'y'  # -dy
                    ying = (y_stem + 'ing')  # -dying
                    if ying in verb_keys:
                        combine(self.VERB, ying, verb)
                        if verb[:-1] + 's' in verb_keys:  # studies
                            combine(self.VERB, verb[:-1] + 's', verb)
                        if y_stem in verb_keys:  # to study
                            combine(self.VERB, y_stem, verb)

    def __group_irreg_verbs(self):
        verb_keys = top_few(self.VERB, 100)
        for verb in verb_keys:
            if len(verb) > 2 and verb[-3:] == 'ing':  # buying, catching (catches, [caught] not catched)
                stem = verb[:-3]
                if not (len(stem) > 0 and stem[-1] == 'e' and stem[:-1] + 'ing' in verb_keys):  # changeing and changing
                    if bool(stem + 's' in verb_keys) ^ bool(stem + 'es' in verb_keys):
                        if stem in verb_keys:
                            combine(self.VERB, stem, verb)
                        if stem + 's' in verb_keys:
                            combine(self.VERB, stem + 's', verb)
                        elif stem + 'es' in verb_keys:
                            combine(self.VERB, stem + 'es', verb)
                            if stem + 'e' in verb_keys:
                                combine(self.VERB, stem + 'e', verb)
                else:
                    combine(self.VERB, verb, stem[:-1] + 'ing')

    def __group_verbs(self):
        self.__group_ed_verbs()
        self.__group_irreg_verbs()

    def __remove_noun_adjectives(self):
        for noun in top_few(self.NOUN, 10) & top_few(self.ADJ, 10):
            if len(noun) > 0 and noun[-1] == 'y':
                del self.NOUN[noun]
            else:
                del self.ADJ[noun]

    def __depluralise_nouns(self):
        noun_keys = top_few(self.NOUN, 50)
        for noun in noun_keys.copy():
            if len(noun) > 0 and noun[-1] == 's' and not (len(noun) > 1 and noun[-2] == 's'):  # end with s not double s
                if len(noun) > 2 and noun[-3:] == 'ies':
                    y_stem = noun[:-3] + 'y'
                    if y_stem in noun_keys:
                        combine(self.NOUN, noun, y_stem)
                        # if y_stem + 's' in noun_keys:
                elif len(noun) > 1 and noun[-2] == 'e' and noun[:-2] in noun_keys:  # branches branch but no cak cakes
                    combine(self.NOUN, noun, noun[:-2])
                elif noun[:-1] in noun_keys:
                    combine(self.NOUN, noun, noun[:-1])
                    noun_keys.remove(noun)  # [Xs, Xses, X, Xse] Xses -> Xse | Xs, dep order

    def __anglicise(self):
        for i in range(3):
            part = self.parts[i]
            suffixes = set(part.keys())
            for american in suffixes:
                if 'z' in american:
                    english = american.replace('z', 's')
                    if english in suffixes:
                        combine(part, american, english)

    def finish(self, trim=4):
        """Aggregate by grouping words sharing the same root together"""
        self.__anglicise()
        self.__remove_noun_adjectives()
        self.__depluralise_nouns()
        self.__group_verbs()
        self.__trim(trim)


def combine(arr, kill, into):
    # print('merging {} into {} from {}'.format(kill, into, arr))
    try:
        arr[into] += arr[kill]
        del arr[kill]
    except KeyError:
        print('died merging {} into {} from {}'.format(kill, into, arr))
        raise


def sort_desc(words):
    return sorted(words, key=lambda w: -words[w])


def top_few(words, num):
    return {w for w in sort_desc(words)[:num]}