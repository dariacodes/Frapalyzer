# coding=utf-8
import sys, itertools
reload(sys)
sys.setdefaultencoding('utf-8')

delim = ';'
newline = '\r\n'
vowels = u"aeiouy\xE2\xE0\xEB\xE9\xEA\xE8\xEF\xEE\xF4\xFB\xF9'"

def first(the_iterable, condition = lambda x: True):
    for i in the_iterable:
        if condition(i):
            return i

def flatmap(lists):
    return [item for l in lists for item in l]

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def powerset(iterable):
    s = list(iterable)
    return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

def grp(data, key, val):
    return [(k, [val(i) for i in gi]) for k, gi in itertools.groupby(sorted(data, key = key), key)]