# coding=utf-8
import codecs, re, os
import apocopes_in_french as aif
from collections import defaultdict
from helpers import *
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()
def stemmed(w):
    s = stemmer.stem(w)
    if not s or len(s) == len(w):
        return w
    return w[:len(s)] + '[' + w[len(s):] + ']'

endings = defaultdict(int)
def ends_inc():
    endings_inc = defaultdict(int)
    for e, c in endings.items():
        for i in range(0, len(e)):
            endings_inc[e[i:]] += c
    return endings_inc
def ends_write_int(dic, path):
    with codecs.open(path, 'w', 'utf-8') as f:
        for ending, count in sorted(dic.items(), key=lambda kv: -kv[1]):
            try:
                f.write(ending + delim + str(count) + newline)
            except:
                pass

def ends_write(name):
    ends_write_int(endings, 'stats/'+name+'-ends.csv')
    #ends_write_int(ends_inc(), 'stats/'+name+'-ends-inc.csv')
def ends_init():
    endings = defaultdict(int)
def ends_add(short, full, pos = ''):
    parts = aif.apo_parts(short, full)
    if parts:
        endings[parts[2]] += 1
        #endings[delim.join([parts[2], pos])] += 1

def inds(a, l):
    return [a[i] for i in l]
#short;full;common;added;cut;ending;is_vocal;pos;len_s;len_f;len_ratio
with codecs.open('data/dict_apo_aug.csv', 'r', 'utf-8') as f:
    augs = [inds(line.strip().split(delim), [0,1,7]) for line in f.readlines()][1:]
#epf = [l for l in [k.split(delim)+[v] for k, v in endings.items()] if l[1] and l[1] != 'nom propre']

ends_init()
for short, full, pos in sorted(augs):
    ends_add(short, full, pos)
ends_write('dict_apo_aug')

def proc_epf():
    with codecs.open('stats/dict_apo_aug-ends.csv', 'r', 'utf-8') as f:
        epf = [[c,p,int(f)] for c,p,f in [line.strip().split(delim) for line in f.readlines()]][1:]

    def pos_cut():
        comE = {l[0] for ll in [sorted(la, key=lambda i: -i[2])[:10] for f, la in grp(epf, lambda p: p[1], lambda p: p)] for l in ll}
        comI = [l for l in epf if l[0] in comE]
        print comI
    pos_cut()

apos = {short for short, full, pos in augs}

#with codecs.open('data/dict_apo_aug_stem.csv', 'w', 'utf-8') as file:
#    for short, full in pairs:
#        try:
#            file.write(stemmed(short)+delim+stemmed(full)+newline)
#        except:
#            print short, full

def gather_stats(words, out, name, n = 500, ends = True):
    if ends:
        ends_init()
    seen = 0
    proc = 0
    with codecs.open(out, 'w', 'utf-8') as file:
        for word in sorted(words):
            seen += 1
            if word in apos:
                continue
            fulls = aif.find_fulls(word)
            if not fulls:
                continue
            if ends:
                for full in fulls:
                    ends_add(word, full)
            file.write(stemmed(word) + delim + ','.join([stemmed(f) for f in fulls]) + newline)

            proc += 1
            if not proc % n:
                print seen, proc, round(100.*seen/len(words))
                if ends:
                    ends_write(name)
    if ends:
        ends_write(name)

#with codecs.open('data/datasets.csv', 'r', 'utf-8') as f:
#    words = {line.lower().strip().split(';')[0] for line in f.readlines()}
with codecs.open('data/list_words.csv', 'r', 'utf-8') as f:
    words = {line.lower().strip('\r\n\t ;,.!?') for line in f.readlines()}
src = 'imp_comp'

def analyse():
    perms = [[1 if i in perm else 0 for i in range(4)] for perm in powerset(range(4))]
    setts = [(perm, src + '_' + ''.join([str(i) for i in perm]), 1) for perm in perms]

    results = []
    for setting in setts:
        methods = setting[0]
        name = setting[1]
        generate = setting[2]
        path = 'stats/' + name + '.csv'

        if generate and not os.path.isfile(path):
            aif.do_blacklist_end, aif.do_blacklist_cut, aif.do_resuffixation, aif.do_stemmer = methods
            gather_stats(words, path, name)
            pass

        try:
            with codecs.open(path, 'r', 'utf-8') as f:
                d = f.read()
            res = (methods, len(re.sub('[^;,]+', '', d)), len(re.sub('[^\n]+', '', d)))
            print setting[0], name, res
            results.append(res)
        except:
            print setting[0], name, 'no data'

    print ([w for m, w, a in results], [a for m, w, a in results], [m for m, w, a in results])
analyse()
