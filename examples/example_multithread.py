#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 06/24/2013, updated 06/24/2013
#
""" Examples of using multithread.py
"""
__all__ = []
print('Executing %s' %  __file__)

import os, sys, time

from poost import parallel

if __name__ == '__main__':

    def _example1():
        # Usage example, abstracted from
        # http://www.ibm.com/developerworks/aix/library/au-threadingpython/
        import time
        import urllib2
        from BeautifulSoup import BeautifulSoup

        # unlike multiprocessing, these worker functions do not have to be
        # placed on the module level

        def urlchunk (host):
            url = urllib2.urlopen(host)
            chunk = url.read()
            return chunk

        def datamine (chunk):
            soup = BeautifulSoup(chunk)
            return soup.findAll(['title'])

        tpc = parallel.ThreadPoolsChain (
            (urlchunk, 4),
            (datamine, 2)
        )

        t0 = time.time()
        results =  tpc.feed([
            "http://google.com",
            "http://yahoo.com",
            "http://google.com",
            "http://amazon.com",
            "http://ibm.com",
            "http://apple.com",
            "http://www.mit.edu",
            "http://www.cs.umn.edu",
        ])
        tpc.stop()

        for i, res in enumerate(results):
            print i, res
        print('Done. Time elapsed: %.2f.' % (time.time() - t0))

    _example1()
