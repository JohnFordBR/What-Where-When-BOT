#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
import pytesseract
import argparse
import re
import os
import unicodedata
import math
def string_length(str1):
    count = 0
    for char in str1:
        count += 1
    return count
indir = 'raw_material/'
for root, dirs, filenames in os.walk(indir):
    for fname in filenames:
        print(fname)
        img = Image.open("raw_material/%s" % fname)
        rawtext = pytesseract.image_to_string(img,lang="rus")
        text=rawtext.encode('utf8')
        nonspace_text=text.replace('\n','')
        try:
            questring = re.search('Вопрос [0-9]+:(.*?)Ответ',nonspace_text).group(0)
            questring = questring.strip()
            comment = re.search('(?<=\Комментарий:)(.*?)(?=\.)',nonspace_text).group(0)
            comment=comment.replace('"','')
            comment = comment.strip()
            file = open("comment/%s.txt" % fname,"w")
            file.write("%s" % comment)
            file.close()
            answer=re.search('(?<=\Ответ:)(.*?)(?=\.)',nonspace_text).group(0)
            answer=answer.replace('"',' ')
            answer=answer.strip()
            quelen= len(questring.decode('utf8'))
            img2 = img.crop((500, 368, 1800, 368.0+math.ceil(quelen/161.0)*17))
            img2.save("questions/%s" % fname)
            file = open("answers/%s.txt" % fname,"w")
            file.write("%s" % answer)
            file.close()
        except:
            print "Caught it!"
