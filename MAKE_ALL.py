# -*- coding: utf-8 -*-
from glob import glob
from subprocess import Popen

for filename in glob ('API_MakeDoc_output\\Live*.xml'):
    version = filename [7:-4]
    if version.count ('.') == 1: version += '.0'
    Popen(('python', 'LiveApiXmlHierarchical.py', filename, version + '.xml')).wait ()

fill_num = lambda version: '.'.join ([num.zfill (2) for num in version.split('.')])
to_compare = [filename for filename in glob ('*.xml') if filename.find ('-') == -1]
for A, B in [(A, B) for A in to_compare for B in to_compare if fill_num (B) > fill_num (A)]:
    Popen(('python', 'CompareXmlTree.py', A, B)).wait ()

Popen(('python', 'MakeIndex.py'))
