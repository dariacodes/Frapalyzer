# coding=utf-8
import codecs, re, os
import apocopes_in_french as aif
from collections import defaultdict
from helpers import *

files = [os.path.join(root, file) for root, dirs, files in os.walk("lepoint") for file in files]
words = defaultdict(int)

rxes = [
    re.compile(u"\s*(Article réservé aux abonnés.*Identifiez-vous)\s*", re.DOTALL|re.U),
    re.compile(u"[^\w']+", re.U),
]
def clean(s, rx = re.compile(u"[^\w']+", re.U)):
    for rx in rxes:
        s = rx.sub(' ', s)
    return s.lower().strip()

for path in files:
    with codecs.open(path, 'r', 'utf-8') as f:
        for word in [word for word in clean(f.read()).split(' ') if word]:
            words[word] += 1

with codecs.open('data/datasets.csv', 'w', 'utf-8') as f:
    for word, count in sorted(words.items(), key = lambda kv: -kv[1]):
        f.write(word + delim + str(count) + newline)
    print 'datasets created'

