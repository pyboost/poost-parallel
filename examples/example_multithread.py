#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 06/24/2013, updated 06/24/2013
#
""" Examples of using multithread.py
"""
__all__ = [

]
print('Executing %s' %  __file__)

import os, sys, time

import poost.parallel as parallel



if __name__ == '__main__':
    t0 = time.time()
    print('Done. Time elapsed: %.2f.' % (time.time() - t0))
