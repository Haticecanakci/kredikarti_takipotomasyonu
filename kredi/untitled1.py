# -*- coding: utf-8 -*-
"""
Created on Fri May 31 22:27:06 2024

@author: hatic
"""


import subprocess

# qrc dosyasını py dosyasına çevirme
subprocess.run(["pyrcc5", "-o", "res_rc.py", "res.qrc"])