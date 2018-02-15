#!/usr/bin/python3

import subprocess
from shutil import copyfile

languages = ['es', 'ja', 'hi', 'pt', 'bn', 'ru', 'de', 'vi', 'ko', 'fr']

file_ori = 'text'
file_tmp = 'fine'
fori = open(file_ori, "r");
ftmp = open(file_tmp, "w");

status = 0
theTitle = ''
trans_zh = ''

count = 0

for line in fori:
    theLine = line.rstrip('\n')

    if theLine == '-------':
        print(count)
        if status > 0 and theTitle != '' and trans_zh != '':
            print('here')
            ftmp.write(theTitle + '\n')
            ftmp.write(trans_zh + '\n')
            for lang in languages:
                translated = subprocess.getoutput('trans -b :' + lang + ' -no-autocorrect "' + theTitle + '"')
                print(translated)
                ftmp.write(translated + '\n')
            theTitle = ''
            trans_zh = ''

            # Screenshot
            #subprocess.call(['./shot/phantomjs', './shot/test.js'])

        status = 1

    elif theLine == '':
        continue

    elif status == 1: # reddit_id
        count = count + 1
        ftmp.write(str(count) + '\n')
        ftmp.write(theLine + '\n')
        status = 2

    elif status == 2:
        theTitle = theLine
        status = 3

    elif status == 3:
        trans_zh = theLine
        status = 2

if theTitle != '' and trans_zh != '':
    ftmp.write(theTitle + '\n')
    ftmp.write(trans_zh + '\n')
    for lang in languages:
        translated = subprocess.getoutput('trans -b :' + lang + ' "' + theTitle + '"')
        print(translated)
        ftmp.write(translated + '\n')

    subprocess.call(['./shot/phantomjs', './shot/take_shot.js', 'ddff'])

fori.close()
ftmp.close()

