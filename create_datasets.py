# coding=utf-8
import codecs, re, os
import apocopes_in_french as aif
from collections import defaultdict
from helpers import *

rxes = [
    re.compile(u"\s*(Article réservé aux abonnés.*Identifiez-vous)\s*", re.DOTALL|re.U),
    re.compile(u"[^\w']+", re.U),
]
def clean(s, rx = re.compile(u"[^\w']+", re.U)):
    for rx in rxes:
        s = rx.sub(' ', s)
    return s.lower().strip()

def proc(beg):
    if os.path.isfile(beg):
        files = [beg]
    else:
        files = [os.path.join(root, file) for root, dirs, files in os.walk(beg) for file in files]
    words = defaultdict(int)

    for path in files:
        with codecs.open(path, 'r', 'utf-8') as f:
            for word in [word for word in clean(f.read()).split(' ') if word]:
                words[word] += 1
    ordered = sorted(words.items(), key = lambda kv: -kv[1])

    if not words:
        print 'No data found'
        return

    data = 'data/datasets.csv'
    with codecs.open(data, 'w', 'utf-8') as f:
        for word, count in ordered:
            f.write(word + delim + str(count) + newline)
    print 'datasets created'
    print "%s distinct words, %s total words" % (len(words), sum(words.values()))
    print "most popular: %s (%s occurences)" % (ordered[0][0], ordered[0][1])

if __name__ == "__main__":
    proc("lepoint")