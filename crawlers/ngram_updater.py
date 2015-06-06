# coding=utf-8
import os, codecs, re, json, shutil
from collections import defaultdict

newline = '\r\n'

curr = 'ngram_data.jsv'
temp = 'ngram_data-new.jsv'
back = 'ngram_data-old.jsv'

with codecs.open(curr, 'r', 'utf-8') as f:
    ds = [d for line in f.readlines() for d in json.loads(line)]
    
fs = defaultdict(int)
for d in ds:
    d["ts_total"] = sum(d["timeseries"])

with codecs.open(temp, 'w', 'utf-8') as f:
    for d in sorted(ds, key = lambda d: d["ngram"]):
        f.write(json.dumps([d]) + newline)

shutil.move(curr, back)
shutil.move(temp, curr)
os.remove(back)
