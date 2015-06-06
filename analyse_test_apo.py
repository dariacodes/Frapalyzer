# coding=utf-8
import codecs, re
import apocopes_in_french as aif
from collections import defaultdict
from helpers import *

def gen_testapo():
    with codecs.open('data/test_apo.csv', 'r', 'utf-8') as inp:
        for short, fulls in [line.strip().split(';') for line in inp.readlines()]:
            for full in fulls.split(','):
                yield short, full

def gen_apoaug():
    with codecs.open('data/dict_apo_aug.csv', 'r', 'utf-8') as inp:
        for short, full in [line.strip().split(';')[:2] for line in inp.readlines()]:
            yield short, full

for query in ['r', 'ment', 'ement', 'que', 'age', 'er', 'ique']:
    for file, gen in {'data/test_apo':gen_testapo, 'data/dict_apo_aug':gen_apoaug}.items():
        with codecs.open('stats/'+file+'Q-'+query+'.csv', 'w', 'utf-8') as out:
            for short, full in gen():
                parts = aif.apo_parts(short, full)
                if parts and parts[2] == query:
                    out.write(short + delim + full + newline)