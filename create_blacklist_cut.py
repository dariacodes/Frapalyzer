# coding=utf-8
import codecs, re, math
from collections import defaultdict
from helpers import *

def create_freqdic(file):
    d = defaultdict(float)
    with codecs.open(file, 'r', 'utf-8') as f:
        for line in f.readlines():
            pair = line.strip().split(delim)[:2]
            d[pair[0]] += float(pair[1])
    total = sum(d.values())
    for k in d:
        d[k] /= total
    return d

def create_histogr(f1, f2):
    hist = defaultdict(float)
    for ending, freq in f1.items():
        hist[ending] += math.log(freq)

    for ending, freq in f2.items():
        hist[ending] -= math.log(freq)
    return hist

def create_histogram(l):
    hist = defaultdict(float)
    for d in l:
        for ending, freq in d.items():
            hist[ending] += freq
    for k,v in hist.items():
        hist[k] = round(v * 10000, 4)
    return hist

daa = create_freqdic('stats/dict_apo_aug-ends.csv')
ta = create_freqdic('stats/TestList_0000-ends.csv')

with codecs.open('data/blacklist_cut.csv', 'w', 'utf-8') as f:
    for apo in {k for k in ta} - {k for k in daa}:
        f.write(delim + apo + newline)
    print 'blacklist_cut created'

with codecs.open('stats/hist.csv', 'w', 'utf-8') as f:
    for k, v in sorted(create_histogram([daa, {k:-v for k, v in ta.items()}]).items(), key = lambda x: x[1]):
        f.write(k + delim + str(v) + newline)