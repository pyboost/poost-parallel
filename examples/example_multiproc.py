#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 07/01/2013, updated 07/01/2013
#
"""
"""
__all__ = []
print('Executing %s' %  __file__)

import sys
import time
import urllib2
from BeautifulSoup import BeautifulSoup

# The worker functions must be placed on the module level, because
# the multiprocessing API have to import this module

def urlchunk (host):
    url = urllib2.urlopen(host)
    chunk = url.read()
    return chunk

def datamine (chunk):
    soup = BeautifulSoup(chunk)
    return soup.findAll(['title'])

# print '__name__==', __name__  # '__parents_main__' if imported by multiprocessing

if __name__ == '__main__':

    # IMPORTANT NOTICE: the construction of ProcessPoolsChain must not carry
    # '__main__' as __name__, because the multiprocessing API will import
    # this module, with __name__=='__parents_main__'.
    # Putting this code on the module level would spawn infinite
    # number of processes!!

    from poost import parallel
    print 'import poost.parallel'

    ppc = parallel.ProcessPoolsChain(
        (urlchunk, 4),
        (datamine, 2)
    )

    t0 = time.time()
    results =  ppc.feed([
        "http://google.com",
        "http://yahoo.com",
        "http://google.com",
        "http://amazon.com",
        "http://ibm.com",
        "http://apple.com",
        "http://www.mit.edu",
        "http://www.cs.umn.edu",
    ])
    ppc.stop()

    for i, res in enumerate(results):
        print i, res
    print('Done. Time elapsed: %.2f.' % (time.time() - t0))

