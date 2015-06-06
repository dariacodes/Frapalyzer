# coding=utf-8
import codecs, re, json, os
import apocopes_in_french as aif
from collections import defaultdict
from helpers import *

delimDef = ';'
newline = '\r\n'

def clean(word):
    rxc = re.compile('\(([^)]*)\)')
    return rxc.sub('\\1', word.strip().strip(' 1234567890`,.?').lower().replace(u"’", u"'")) #remove brackets


def json_to_csv(src, dst, sKey = 'apo', fKey = 'full'):
    with open(src) as data_file:
        data = json.load(data_file)
    with codecs.open(dst, 'w', 'utf-8') as newWords:
        for l in data:
            full = clean(l[fKey])
            short = clean(l[sKey])
            if 1 < len(short.split()):
                continue
            for fu in [clean(f) for f in full.split(',')]:
                if fu != short and fu[:2] == short[:2]:
                    newWords.write(delimDef.join([short, fu]) + newline)

json_to_csv('crawlers/cnrtl.json','sources/cnrtl.csv')
json_to_csv('crawlers/echolalie.json','sources/echolalie.csv')

def append_apocopes(path, delim = '\t'):
    apos_curr = set()
    with codecs.open(path, 'r', 'utf-8') as i:
        for line in i.readlines():
            short, full = line.split(delim)[:2]
            apos_curr.add((clean(short), clean(full)))
    return apos_curr

sources = [
    ('sources/legrandrobert.tsv', '\t'),
    ('sources/wiktionary.csv', ';'),
    ('sources/cnrtl.csv', ';'),
    ('sources/echolalie.csv', ';'),
    ('sources/piechnik.csv', ';'),
    ('sources/languefr.csv', ';'),
    ('sources/finallyover.csv', ';'),
]
fpairs = {re.sub(ur'^.*?/([^/.]*?)(\..*)?$', ur'\1', file): append_apocopes(file, sep) for file, sep in sources}

def check(short, full, regExp = re.compile('\\s')):
    return not (len(full) <= len(short) or regExp.search(full) != None or regExp.search(short) != None)
def gen_good_bad(fps):
    fgbs = {}
    for f, ps in fps.items():
        goods = set()
        bads = set()
        for short, full in ps:
            if check(short, full) and aif.is_apocope_of(short, full):
                goods.add((short, full))
            else:
                bads.add((short, full))
        fgbs[f] = (goods, bads)
    return [
        {'gud'+delimDef+f: gb[0] for f, gb in fgbs.items()},
        {'bad'+delimDef+f: gb[1] for f, gb in fgbs.items()},
    ]

def gen_apos_pairs(fps):
    return [
        {'pars'+delimDef+f: ps for f, ps in fps.items()},
        {'apos'+delimDef+f: {s for s, f in ps} for f, ps in fps.items()},
    ]

def gen_unique_exclusive_total(d):
    return [
        [('unq'+delimDef+f, len(s)) for f, s in d.items()],
        [('exc'+delimDef+f, len(s - {w for ss in d.values() if ss != s for w in ss})) for f, s in d.items()],
        [('   '+delimDef+re.sub(ur';([^;]+)$', ur';total', f), len({s for ss in d.values() for s in ss}))],
    ]

fgs, fbs = gen_good_bad(fpairs)
def make_files(details = False):
    for path, d in {'data/dict_apo_auto.csv': fgs, 'data/dict_apo_auto_bad.csv': fbs}.items():
        with codecs.open(path, 'w', 'utf-8') as f:
            for short, full in sorted({s for ss in d.values() for s in ss}):
                buf = delimDef.join([short, full]) + newline
                f.write(buf)
        if details:
            for file, ss in d.items():
                with codecs.open('stats/'+path+'.'+file, 'w', 'utf-8') as f:
                    for short, full in sorted(ss):
                        buf = delimDef.join([short, full]) + newline
                        f.write(buf)
make_files()
print 'dict_apo_auto created'

stats = [stat for gbl in [fgs, fbs] for d in gen_apos_pairs(gbl) for stat in gen_unique_exclusive_total(d)]

for stat in stats:
    print '\r\n' + '\r\n'.join([';'.join([f, str(l)]) for f, l in sorted(stat, key=lambda kv: -kv[1])])

def backup():
    with codecs.open('data/dict_apo_auto.csv', 'r', 'utf-8') as d:
        with codecs.open('data/dict_apo_auto_regress.csv', 'w', 'utf-8') as dregress:
            shorts = set()
            for line in d:
                short = line.split(';')[0]
                shorts.add(short)
            dregress.write('\r\n'.join(sorted(shorts)))
def regress_errors():
    with codecs.open('data/dict_apo_auto.csv', 'r', 'utf-8') as f:
        curr = {s.split(';')[0].strip() for s in f.readlines()}

    regress_f = 'data/dict_apo_auto_regress.csv'
    if not os.path.isfile(regress_f):
        prev = set()
    else:
        with codecs.open(regress_f, 'r', 'utf-8') as f:
            prev = {s.strip() for s in f.readlines()}

    created = list(sorted(curr - prev))
    deleted = list(sorted(prev - curr))
    return created, deleted

news, errors = regress_errors()
if news:
    print "Found new apos:"
    for n in sorted(news):
        print "\t" + n
if errors:
    for m in sorted(errors):
        print m
    raise Exception("Lost %s apocopes" % len(errors))
else:
    backup()

aif.reload_dictionary()