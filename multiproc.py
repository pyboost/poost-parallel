#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 06/24/2013, updated 06/24/2013
#
""" Helper functions and templates for multiprocessing.

    http://hg.python.org/cpython/file/3.3/Lib/concurrent/futures/process.py
"""
__all__ = [

]
print('Executing %s' %  __file__)

import os, sys, time
from multiprocessing import Manager, Process, Pool, Pipe, Queue


if __name__ == '__main__':
    t0 = time.time()
    print('Done. Time elapsed: %.2f.' % (time.time() - t0))
