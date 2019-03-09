#!/usr/bin/env python
__author__ = 'justinarmstrong'

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import sys
import pygame as pg
from data.main import main
import cProfile

from data.connect import THREAD

if __name__=='__main__':
    THREAD.start()
    main()
    pg.quit()
    sys.exit()
