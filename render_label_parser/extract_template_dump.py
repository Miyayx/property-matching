# -*- coding:utf-8 -*-

import codecs
import re
import os

"""
把dump文件中关于Template的部分抽取出来，做进一步处理用
"""

def extract_template_dump(fi):
    TITLE_REGEX = r'<title>(.+)</title>'
    DIR, filename = fi.rsplit('/',1)
    wiki, time = filename.split('-')[:2]
    fw = codecs.open(DIR+'/'+wiki+'-'+time+'-template-dump.dat', 'w')

    n = 0
    
    fr = codecs.open(fi)
    line = fr.readline()
    while line:
        if re.search(TITLE_REGEX, line):
            title = re.findall(TITLE_REGEX, line)[0].strip()
            if title.startswith('Template:PRC admin/'):
                line = fr.readline()
                continue
            if title.startswith('Template:') or title.startswith('模板'):
                print "Recording "+title+"..."
                n += 1
                fw.write('<page>\n')
                while not '</page>' in line:
                    fw.write(line)
                    line = fr.readline()
                fw.write('</page>\n')
        line = fr.readline()
    fw.close()
    print n,'templates'


if __name__=='__main__':
    import sys
    fi = sys.argv[1]
    extract_template_dump(fi)
