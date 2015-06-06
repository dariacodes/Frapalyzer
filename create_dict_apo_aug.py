# coding=utf-8
import codecs, re, sys
import apocopes_in_french as aif
from helpers import *
from collections import defaultdict

aposAug = {}
headers = []

with codecs.open('data/dict_apo_auto.csv', 'r', 'utf-8') as i:
    for line in i.readlines():
        short, full = line.strip().split(delim)[:2]
        aposAug[(short, full)] = { 'short': short, 'full': full }

with codecs.open('data/dict_apo_man.csv', 'r', 'utf-8') as i:
    for line in i.readlines():
        if not headers:
            headers = line.strip().split(delim)
            continue
        data = line.strip().split(delim)
        apo = {}
        for i in range(len(headers)):
            apo[headers[i]] = data[i]
        key = (apo['short'], apo['full'])
        if key in aposAug:
            aposAug[key] = apo

stats = defaultdict(lambda: defaultdict(int))
def add_stat(key, value):
    stats[key][value] += 1

for apo in aposAug.values():
    apo['len_s'] = len(apo['short'])
    apo['len_f'] = len(apo['full'])
    apo['len_ratio'] = int(100. * apo['len_f'] / apo['len_s']) / 100.
    path = aif.is_apocope_of(apo['short'], apo['full'])
    if not path:
        print apo
    #apo['path'] = path[:-1] if path else []
    apo['ending'] = apo['short'][-1]
    apo['is_vocal'] = apo['ending'] in vowels

    statParts = aif.apo_parts(apo['short'], apo['full'])
    if statParts:
        apo['common'] = statParts[0]
        apo['added'] = statParts[1]
        apo['cut'] = statParts[2]
        apo['is_vocal'] = apo['common'][-1] in vowels

    add_stat('is_vocal', apo['is_vocal'])
    add_stat('ending', apo['ending'])
    if 'pos' in apo:
        add_stat('pos', apo['pos'])
        add_stat('pos-end', (  apo['pos'].split(' ')[0], apo['ending']))

cuts = {}
for apo in aposAug.values():
    cut = apo['cut']
    added = apo['added']
    if not added:
        added = apo['ending']

    replacements = {'que' : ['ique', 'ematique', 'itique', 'eptique']}
    kv = first(replacements.items(), lambda kv: cut in kv[1])
    if kv:
        cut = kv[0]

    if cut not in cuts:
        cuts[cut] = [set(), 0]
    cuts[cut][0].add(added)
    cuts[cut][1] += 1

with codecs.open('stats/cuts.csv', 'w', 'utf-8') as f:
    for cut, s in sorted(cuts.items(), key=lambda kv: kv[0][::-1]):
        f.write(cut.rjust(15) + ';' + str(s[1]).rjust(5) + ';' + str(s[0]) + '\r\n')

def create_stat():
    for stat, data in stats.items():
        with codecs.open('stats/stat_' + stat + '.csv', 'w', 'utf-8') as f:
            for (key, freq) in sorted(data.items(), key=lambda x: x if type(x) is tuple else -x[1]):
                f.write((key if type(key) is basestring else ';'.join(key) if type(key) is tuple else str(key)) + ';' + str(freq) + '\n')
create_stat()

#print stats

def create_aug(f, flt = lambda _: True):
    with codecs.open(f, 'w', 'utf-8') as file:
        keys = ['short', 'full', 'common', 'added', 'cut', 'ending', 'is_vocal', 'pos', 'len_s', 'len_f', 'len_ratio']
        for _, apo in aposAug.items():
            for key in apo:
                if key not in keys:
                    keys.append(key)
        file.write(delim.join(keys) + newline)
        for _, apo in sorted(aposAug.items()):
            if not flt(apo):
                continue
            items = []
            for key in keys:
                if key not in apo:
                    items.append('')
                elif isinstance(apo[key], basestring):
                    items.append(apo[key])
                else:
                    items.append(str(apo[key]))
            file.write(delim.join(items) + newline)

def create_statParts(f, col = 'added'):
    with codecs.open(f, 'w', 'utf-8') as file:
        keys = [col, 'cut', 'short', 'full']
        file.write(delim.join(keys) + newline)
        for _, apo in sorted(aposAug.items(), key=lambda kv: (kv[1]['cut'][::-1], kv[1][col])):
            if col not in apo or not apo[col]:
                continue
            items = []
            for key in keys:
                if key not in apo:
                    items.append('')
                else:
                    items.append(apo[key].rjust(15))
            file.write(delim.join(items) + newline)

create_aug('data/dict_apo_aug.csv')
print 'dict_apo_aug created'
create_aug('stats/dict_apo_aug_flt_added.csv', lambda apo: apo['added'])

create_statParts('stats/dict_apo_aug_stat_parts.csv')
create_statParts('stats/dict_apo_aug_stat_parts_e.csv', 'ending')