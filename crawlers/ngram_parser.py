# coding=utf-8
import os, codecs, re, urllib, urllib2, json, time, random
from lxml.html import parse, etree
from collections import defaultdict

delim = ';'
newline = '\r\n'

def find_freqs(words):
    processed = set()
    try:
        with codecs.open('ngram_data.jsv', 'r', 'utf-8') as f:
            processed = {d["url"] for l in f.readlines() for d in json.loads(l)}
    except Exception as e:
        print e

    extractor = re.compile(u'var data[^[]+(\[.*?\]);', re.U)
    cleaner = re.compile(u'\s*\(All\)$', re.U)
    template = "https://books.google.com/ngrams/graph?content=%s&case_insensitive=on&year_start=%s&year_end=%s&corpus=19"
    year_start = 1500
    year_end = 2008

    with codecs.open('ngram_data.jsv', 'a', 'utf-8') as f:
        random.shuffle(words)
        for word in words:
            try:
                url = template % (urllib.quote_plus((word).encode('utf8')), year_start, year_end)
                if url in processed:
                    continue
                print 'Parsing: %s' % url
                page = urllib2.urlopen(url).read()
                data = json.loads(extractor.findall(page)[0])
                data = [d for d in data if d["type"] == 'CASE_INSENSITIVE']
                if not data:
                    continue
                for d in data:
                    d["year_start"] = year_start
                    d["year_end"] = year_end
                    d["ngram"] = cleaner.sub('', d["ngram"])
                    d["url"] = url
                    d["word"] = word
                f.write(json.dumps(data) + '\r\n')
                print ', '.join([d["ngram"] for d in data])
            except:
                pass
            time.sleep(1)

def create_file(dic, fileName):
    if not dic:
        return
    with codecs.open(fileName, 'w', 'utf-8') as file:
        for short in sorted(dic):
            for full in dic[short]:
                file.write(delim.join([short, full]) + newline)

if __name__ == '__main__':
    apos = defaultdict(list)
    with codecs.open('../dict_apo_auto.csv', 'r', 'utf-8') as d:
        for line in d:
            pairs = line.strip().split(delim)
            apos[pairs[0]].append(pairs[1])
    find_freqs(sorted({w for a, fl in apos.items() for f in fl for w in [a, f]}))
