#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 06/24/2013, updated 06/24/2013
#
""" Helper functions and templates for multi-threading code.

    References:
    http://www.ibm.com/developerworks/aix/library/au-threadingpython/
    http://wiki.python.org/moin/PythonDecoratorLibrary#Asynchronous_Call

"""
__all__ = [
    'GenericThread',
    'async_chained',
]
print('Executing %s' %  __file__)

import os, sys, time
import Queue
import threading


class GenericThread (threading.Thread):

    def __init__ (self, func, inque, outque):
        threading.Thread.__init__(self)
        self.func = func
        self.inque = inque
        self.outque = outque

    def run (self):
        while True:
            index, item = self.inque.get()  # blocking
            output = self.func(item)
            self.outque.put((index, output))
            self.inque.task_done()


def async_chained (input_list, func_list, workers_list):

    numpools = len(func_list)
    output_list = [None for _ in xrange(len(input_list))]

    queues = [Queue.Queue() for _ in xrange(numpools + 1)]

    for index, item in enumerate(input_list):
        queues[0].put((index, item))

    for i_pool in range(numpools):
        func = func_list[i_pool]
        for j_worker in range(workers_list[i_pool]):
            t = GenericThread(func, queues[i_pool], outque=queues[i_pool+1])
            t.daemon = True
            t.start()

    # join/sync on the final output queue
    finished_indices = set()
    while len(finished_indices) < len(output_list):
        index, result = queues[-1].get()  # blocking
        output_list[index] = result
        finished_indices.add(index)
        queues[-1].task_done()

    #for i_pool in range(numpools+1):
    #    queues[i_pool].join()

    return output_list


if __name__ == '__main__':
    # Usage example, abstracted from
    # http://www.ibm.com/developerworks/aix/library/au-threadingpython/

    import time
    import urllib2
    from BeautifulSoup import BeautifulSoup

    t0 = time.time()

    def urlchunk (host):
        url = urllib2.urlopen(host)
        chunk = url.read()
        return chunk

    def datamine(chunk):
        soup = BeautifulSoup(chunk)
        return soup.findAll(['title'])


    hosts = ["http://yahoo.com",
             "http://google.com",
             "http://amazon.com",
             "http://ibm.com",
             "http://apple.com"]
    funcs = [urlchunk, datamine]
    workers = [2, 2]
    results = async_chained (hosts, func_list=funcs, workers_list=workers)
    for i, res in enumerate(results):
        print i, res

    print('Done. Time elapsed: %.2f.' % (time.time() - t0))
