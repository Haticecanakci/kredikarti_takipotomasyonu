# -*- coding: utf-8 -*-
"""
Created on Wed May 22 21:48:07 2024

@author: hatic
"""

from PyQt5 import uic

with open("widgets.py","w", encoding="utf-8") as fout:
    uic.compileUi("otomasyon.ui", fout)
    
# -*- coding: utf-8 -*-

