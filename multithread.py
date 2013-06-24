#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 06/24/2013, updated 06/24/2013
#
""" Helper functions and templates for multi-threading code.
"""
__all__ = [

]
print('Executing %s' %  __file__)

import os, sys, time
import Queue
import threading


if __name__ == '__main__':
    t0 = time.time()
    print('Done. Time elapsed: %.2f.' % (time.time() - t0))
