# coding=utf-8
import os, codecs, re
from lxml.html import parse, etree

delim = ';'
newline = '\r\n'

extractor = re.compile(ur"^[\w\W]*(?:[Aa]pocope|[Aa]brév(?:\.|iation)) +d[e'] +(\w+?) +[\w\W]*$", re.U)

def get_apocopes(url):
    def cleaner(f, apo):
        f = f.lower().split(';')[0]
        repl = re.compile(ur"^\W*([\w' \-\.]+)\s*(?:\(\.*?\))*.*$", re.U)
        f = repl.sub(ur"\1", f)
        if ',' in f:
            print ', in ' + f
            for full in f.split(','):
                full = full.strip()
                if full[:3] == apo[:3]:
                    return full
        return f

    apo_urls = []
    for node in parse(url).findall('.//div[@class="fpltemplate"].//li/a[@class="wikilink"]'):
        apo_urls.append((node.tail.strip(), node.attrib['href']))

    with codecs.open('languefr.log', 'w', 'utf-8') as log:
        apos = {}
        for short, url in sorted(apo_urls):
            short = short.lower().strip()
            if short not in apos:
                apos[short] = set()
            fulls = apos[short]

            url_parsed = parse(url)
            for node in url_parsed.findall('.//div[@id="wikitext"].//p'):
                text = node.text
                if text:
                    m = extractor.search(text)
                    if m:
                        fulls.add(cleaner(m.group(1), short))

            if not fulls:
                found = url_parsed.findall('.//div[@id="wikitext"].//p/span[@class="article-lead"]')
                if found:
                    full = found[0].text
                    fulls.add(cleaner(full, short))
                else:
                    log.write(short + delim + ' + '.join(fulls) + newline)
    return apos

def create_file(dic, fileName):
    if not dic:
        return
    with codecs.open(fileName, 'w', 'utf-8') as file:
        for short in sorted(dic):
            for full in dic[short]:
                file.write(delim.join([short, full]) + newline)

if __name__ == '__main__':
    apos = get_apocopes(u"http://www.languefrancaise.net/Morphologie/2")
    create_file(apos, 'languefr.csv')