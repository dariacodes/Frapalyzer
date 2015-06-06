# coding=utf-8
import os, codecs, re
from lxml.html import parse, etree

delim = ';'
newline = '\r\n'
extractor = re.compile(u'(?:(?:du mot |de |d’)(.+?),? par apocope|(?:apocope|début|abréviation) (?:phonétique |argotique )?(?:de |du mot |des prénoms |pour |d’|)(.+?)(?: (?:et|ou) (.+?))?)\.?$', re.U)
cleaner = re.compile(u'^(?:de\s|d’|l’argot\s|l’espagnol\s|l’anglais\s|l’allemand\s|l’expression\s|l’adjectif\s|ce\smot\sdonne )?(?:«\s*)?(.*?)(?:\s*»)?(?:\savec\s.*|\ssous\s.*|\sau\ssens\s.*|\sainsi\sque\s.*|\sdans\sle\smot\s.*|\s*?[;,.→].*|\s\([^)]*?\)|\s\[\d+\])*$', re.U);

def get_apocopes(list_urls):
    apo_urls = []
    for list_url in list_urls:
        for node in parse(list_url).findall('.//div[@class="mw-category"].//li/a[@href]'):
            apo_urls.append((node.text, 'http://fr.wiktionary.org' + node.attrib['href']))
    
    with codecs.open('wiki.log', 'w', 'utf-8') as log:
        apos = {}
        for short, url in sorted(apo_urls):
            short = short.lower()
            if short not in apos:
                apos[short] = []
            fulls = apos[short]
            for node in parse(url).findall('.//dl/dd'): #/i/a[@href]
                text = etree.tostring(node, encoding = 'unicode', method = "text").lower().replace('\n', '')
                fulls_sub = []
                for match in extractor.findall(text):
                    for full in match:
                        full = cleaner.sub('\\1', full)
                        if not full:
                            continue
                        fulls_sub.append(full)
                log.write(delim.join([short, str(fulls_sub), text]) + newline)
                if not fulls_sub:
                    print short, '=>', text
                    continue
                for full in fulls_sub:
                    if full not in fulls:
                        fulls.append(full)
    return apos

def create_file(dic, fileName):
    if not dic:
        return
    with codecs.open(fileName, 'w', 'utf-8') as file:
        for short in sorted(dic):
            for full in dic[short]:
                file.write(delim.join([short, full]) + newline)

if __name__ == '__main__':
    urls = [u"http://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Apocopes_en_fran%C3%A7ais", 
    u"http://fr.wiktionary.org/w/index.php?title=Cat%C3%A9gorie:Apocopes_en_fran%C3%A7ais&pagefrom=periph%0Ap%C3%A9riph#mw-pages",
    u"http://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Apocopes_famili%C3%A8res_en_fran%C3%A7ais"]
    apos = get_apocopes(urls)
    create_file(apos, 'wiktionary.csv')
