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
    http://hg.python.org/cpython/file/3.3/Lib/concurrent/futures/thread.py

"""
__all__ = [
    'WorkerThread',
    'ThreadPoolChain',
]
print('Executing %s' %  __file__)

import Queue
import threading


class WorkerThread (threading.Thread):
    """ A worker thread that gets data from an input queue, calls a specified
        function, and puts the (indexed) result into an output queue.
    """
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


class ThreadPoolChain (object):
    """ Asynchronous worker-thread pools chained by queues.
    """
    def __init__ (self, *funcs_workers):
        """ Constructor for ThreadPoolChain.
            e.g. ThreadPoolchain( (func1, num1), (func2, num2) )
            means num1 workers for func1, num2 workers for func2.
        """
        numpools = len(funcs_workers)
        #self.pools = [[] for _ in xrange(numpools)]
        self.queues = [Queue.Queue() for _ in xrange(numpools + 1)]
        for i, (func, numworkers) in enumerate(funcs_workers):
            for _ in range(numworkers):
                t = WorkerThread (func, self.queues[i], self.queues[i+1])
                t.daemon = True
                t.start()
                #self.pools[i].append(t)

    def feed (self, inputs):
        """ Feeds a sequence of data into the input queue, and obtains a
            sequence of outputs that match the input order.
        """
        numinputs = len(inputs)
        outputs = [None for _ in xrange(numinputs)]
        for index, item in enumerate(inputs):
            self.queues[0].put((index, item))

        # manually join/sync on the final output queue
        finished = set()
        while len(finished) < len(outputs):
            index, result = self.queues[-1].get()  # blocking
            outputs[index] = result
            finished.add(index)
            self.queues[-1].task_done()

        # maybe unnecessary
        #for i in range(len(self.pools)+1):
        #    self.queues[i].join()
        return outputs


if __name__ == '__main__':

    def _example1():
        # Usage example, abstracted from
        # http://www.ibm.com/developerworks/aix/library/au-threadingpython/
        import time
        import urllib2
        from BeautifulSoup import BeautifulSoup

        def urlchunk (host):
            url = urllib2.urlopen(host)
            chunk = url.read()
            return chunk

        def datamine (chunk):
            soup = BeautifulSoup(chunk)
            return soup.findAll(['title'])

        tpc = ThreadPoolChain (
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
        for i, res in enumerate(results):
            print i, res
        print('Done. Time elapsed: %.2f.' % (time.time() - t0))

    _example1()
