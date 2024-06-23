# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:32:37 2024

@author: hatic
"""

from PyQt5 import uic

with open("hakkinda.py","w", encoding="utf-8") as fout:
    uic.compileUi("Hakkinda.ui", fout)