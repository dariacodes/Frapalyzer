# coding=utf-8
import codecs, re, os
from helpers import *
from collections import defaultdict
from nltk.stem.snowball import FrenchStemmer

prefixes = ["j'", "m'", "t'", "l'", "d'", "c'", "qu'", "n'"]
rem_prefix = re.compile(u"^("+'|'.join(prefixes)+")", re.U)

refs = {
    re.compile(u"é(?!e?$)|è|ê|ë|'(?=$)|’(?=$)", re.U): "e",
    re.compile(u"ô", re.U): "o",
    re.compile(u"ï|î", re.U): "i",
    re.compile(u"û|ù", re.U): "u",
    re.compile(u"â|à", re.U): "a",
    re.compile(u"[-]", re.U): "",
    re.compile(u"ph|ff", re.U): "f",
    re.compile(u"ks", re.U): "x",
}
def sdex(word):
    for ref, rep in refs.items():
        word = ref.sub(rep, word)
    return word

def indexer(word):
    return sdex(word)[:2]
index = defaultdict(list)

def apo_parts(short, full, reStatParts = re.compile(ur'^(.+)(.*);\1(.+)$', re.U)):
    def clean(apo):
        return sdex(rem_prefix.sub('', apo))
    cleaned = clean(short) + ';' + clean(full)
    parts = reStatParts.findall(cleaned)
    if parts:
        return parts[0][0], parts[0][1], parts[0][2]
    else:
        print cleaned

dictionary = []
def reload_dictionary(path = 'data/list_words.csv'):
    del dictionary[:]
    with codecs.open(path, 'r', 'utf-8') as f:
        for line in f.readlines():
            dictionary.append(line.strip())
    index.clear()
    for w in dictionary:
        index[indexer(w)].append(w)
reload_dictionary()

blacklist_end_f = 'data/blacklist_end.csv'
blacklist_end = []
if not os.path.isfile(blacklist_end_f):
    print blacklist_end_f + ' is missing'
else:
    with codecs.open(blacklist_end_f, 'r', 'utf-8') as i:
        for line in [line.strip() for line in i.readlines()]:
            if not line or line[0] == '#':
                continue
            blacklist_end.append(line)

blacklist_cut_f = 'data/blacklist_cut.csv'
blacklist_cut = {}
if not os.path.isfile(blacklist_cut_f):
    print blacklist_cut_f + ' is missing'
else:
    with codecs.open(blacklist_cut_f, 'r', 'utf-8') as i:
        for line in [line.strip().split(';') for line in i.readlines()]:
            if not line or line[0] == '#':
                continue
            reg_apo_sub, cut_mask = re.compile(line[0], re.U), line[1]
            blacklist_cut[cut_mask] = reg_apo_sub

def cuts_in_blacklist(w, f):
    #restrictions for cuts of the full
    parts = apo_parts(w, f)
    if not parts:
        return False
    cut = parts[2]
    if cut not in blacklist_cut:
        return False
    if blacklist_cut[cut].match(w):
        return True
    return False

blacklist_endings = [('', 'ette'), ('ion', ''), ('ie', ''), ('que', 'quement'), ('able', 'ablement'), ('', 'oche'), ('', 'alement'), ('', 'inement'), ('ent', 'entement')]

def is_apocope(word):
    return any(find_fulls_int(word))

def find_fulls(apo):
    return [x for x in find_fulls_int(apo)]

do_blacklist_end = True
do_blacklist_cut = True
do_resuffixation = True
do_stemmer = True
stemmer = FrenchStemmer()
def find_fulls_int(apo):
    apo = rem_prefix.sub('', apo)
    if apo in blacklist_end:
        return
    for full in index[indexer(apo)]:
        if is_apocope_of(apo, full) \
        and (not do_blacklist_cut or not cuts_in_blacklist(apo, full)) \
        and (not do_stemmer or stemmer.stem(apo) != stemmer.stem(full)):
            yield full


def apo_endings(apo, rec = re.compile(u"(os|[oesut'.]|’)$", re.U)):
    sub = rec.sub('', apo)
    return sub, apo[len(sub):]

def is_apocope_of(word, full):
    if len(full) <= len(word) or word == full:
        return False

    def nothing(s, f):
        return s, f
    def has_bad_ending(s, f):
        if not do_blacklist_end:
            return s, f
        for apo_end, full_end in blacklist_endings:
            if s.endswith(apo_end) and f.endswith(full_end):
                raise Exception('blacklisted')
        return s, f
    def plurals(s, f):
        if s.endswith('s'):
            s = s[:-1]
        if f.endswith('s'):
            f = f[:-1]
        return s, f
    def extended(s, f):
        s, trunc = apo_endings(s)
        if do_resuffixation and trunc and s[-1] in vowels:
            raise Exception('resuffixation of vocal apocope')
        return s, f
    def soundex(s, f):
        return sdex(s), sdex(f)

    try:
        stages = [nothing, has_bad_ending, plurals, extended, soundex]
        for stage in stages:
            word, full = stage(word, full)
            if word == full[:len(word)]:
                return True
    except:
        return False

    return False
