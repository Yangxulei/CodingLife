#!/usr/bin/env python3

import re
import string
import sys
import os
import argparse
from collections import Counter

__all__ = ['WordFinder', 'Book']

lemmas = {}
with open('lemmas.txt') as fin:
    for line in fin:
        line = line.strip()
        headword = line.split('\t')[0]
        try:
            related = line.split('\t')[1]
        except IndexError:
            related = None
        lemmas[headword] = related


valid_words = set()
for headword, related in lemmas.items():
    valid_words.add(headword)
    if related:
        valid_words.update(set(related.split()))


class WordFinder(object):

    def __init__(self):

        self.main_table = {}
        for char in string.ascii_lowercase:
            self.main_table[char] = {}
        self.special_table = {}

        for headword, related in lemmas.items():

            headword = headword.lower()
            try:
                related = related.lower()
            except AttributeError:
                related = None
            if related:
                for word in related.split():
                    if word[0] != headword[0]:
                        self.special_table[headword] = set(related.split())
                        break
                else:
                    self.main_table[headword[0]][headword] = set(related.split())
            else:
                self.main_table[headword[0]][headword] = None

    def find_headword(self, word):
        """Search the 'table' and return the original form of a word"""
        word = word.lower()
        alpha_table = self.main_table[word[0]]
        if word in alpha_table:
            return word

        for headword, related in alpha_table.items():
            if related and (word in related):
                return headword

        for headword, related in self.special_table.items():
            if word == headword:
                return word
            if word in related:
                return headword

        return None

    # TODO
    def find_related(self, headword):
        pass


def is_dirt(word):
    return word not in valid_words


def list_dedup(list_object):

    temp_list = []
    for item in list_object:
        if item not in temp_list:
            temp_list.append(item)
    return temp_list


class Book(object):
    def __init__(self, filepath):
        with open(filepath) as bookfile:
            content = bookfile.read().lower()
            self.temp_list = re.split(r'\b([a-zA-Z-]+)\b', content)
            self.temp_list = [item for item in self.temp_list if not is_dirt(item)]
            finder = WordFinder()
            self.temp_list = [finder.find_headword(item) for item in self.temp_list]

    def frequency(self):

        cnt = Counter()
        for word in self.temp_list:
            cnt[word] += 1
        return cnt

    # TODO
    def stat(self):
        pass


if __name__ == '__main__':
    if sys.platform == 'nt':
        sys.stderr.write("I haven't tested the code on Windows. Feedback is welcome.\n")

    LINE_SEP = os.linesep

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input_file')
    parser.add_argument('-o', '--output', dest='output_file')
    args = parser.parse_args()

    book = Book(args.input_file)
    result = book.frequency()

    max_width = max(len(str(v)) for v in result.values())

    report = []
    for word in sorted(result, key=lambda x: result[x], reverse=True):
        report.append('{:>{}} {}'.format(result[word], max_width, word))

    if args.output_file:
        with open(args.output_file, 'w') as output:
            output.write(LINE_SEP.join(report))
            output.write(LINE_SEP)
    else:
        print(LINE_SEP.join(report))
