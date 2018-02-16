#!/usr/bin/python3

import subprocess
from shutil import copyfile

file_org = 'text'
file_tmp = '20.tmp'
fori = open(file_org, "r");
ftmp = open(file_tmp, "w");

status = 0
theTitle = ''
trans_zh = ''

for line in fori:
    theLine = line.rstrip('\n')

    # After translating

    if status == 3:
        ftmp.write(theLine + '\n')
        continue

    # Before translating

    if theLine == '-------':
        ftmp.write(theLine + '\n')
        status = 1

    elif theLine == '':
        if status == 12:
            # Translate it
            print(theTitle)
            translated = subprocess.getoutput('trans -b :zh -no-autocorrect "' + theTitle + '"')
            ftmp.write(translated + '\n\n')
            status = 3
        else:
            ftmp.write('\n')

    else:
        if status == 1:
            ftmp.write(theLine + '\n')
            status = 11
        elif status == 11: # trans_zh
            ftmp.write(theLine + '\n')
            theTitle = theLine # May translate it
            status = 12
        elif status == 12: # trans_zh
            ftmp.write(theLine + '\n')
            trans_zh = theLine
            status = 11

fori.close()
ftmp.close()

copyfile('20.tmp', 'text')
