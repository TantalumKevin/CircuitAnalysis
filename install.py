import os
from pip._internal import main

path = __file__.replace("install.py","")
main(['install', '-r', path + 'requirements.txt'])