#coding:utf8

import database
import re


def main():

    Database = database.Database_capture()
    try:
        f = open('sitemap_lect_1.xml','r')
        for line in f.readlines():
        #print(line.strip())
            m = re.match(r'^<loc>(.*)</loc>$',line.strip())
        #m = re.search(r'<loc>.*',line.strip())
            if m:
            #print "yse"
                contact = re.search(r'contact.html',m.group(1))
                if contact:
                    pattern_key = re.compile('([0-9]{6,7})',re.S)
                    items_key = re.findall(pattern_key, m.group(1))
                    print m.group(1),'  ',items_key[0]
                    #getUrl(m.group(1))
                    Database.saveDataUrl(m.group(1),items_key[0])
        Database.close()
    finally:
        if f:
            f.close()

if __name__ == '__main__':
    main()