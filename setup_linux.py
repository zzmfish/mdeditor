#!/usr/bin/env pythonc
import os

if not os.path.exists('plantuml.jar'):
    os.system('wget http://nchc.dl.sourceforge.net/project/plantuml/plantuml.jar')

dot_path = os.popen('which dot').read()
if not dot_path:
    print 'install graphviz'
    os.system('sudo apt-get install graphviz')

try:
    import pygments
except ImportError:
    os.system('sudo apt-get install python-pygments')

os.system('git submodule init')
os.system('git submodule update')
