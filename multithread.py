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
    'ThreadPoolsChain',
]
print('Executing %s' %  __file__)

import Queue
import threading


def worker (func, inque, outque):
    """ A worker thread that gets data from an input queue, calls a specified
        function, and puts the (indexed) result into an output queue.
    """
    for index, item in iter(inque.get, '__STOP__'):
        # inque.get is called until it returns the sentinel
        output = func(item)
        outque.put((index, output))
        inque.task_done()
    #print 'died'


class ThreadPoolsChain (object):
    """ Asynchronous worker-thread pools chained by queues.
    """
    def __init__ (self, *funcs_workers):
        """ Constructor for ThreadPoolChain.
            e.g. ThreadPoolchain( (func1, num1), (func2, num2) )
            means num1 workers for func1, num2 workers for func2.
        """
        self.numpools = len(funcs_workers)
        self.numworkerslist = []
        #self.pools = [[] for _ in xrange(numpools)]
        self.queues = [Queue.Queue() for _ in xrange(self.numpools + 1)]
        for i, (func, numworkers) in enumerate(funcs_workers):
            self.numworkerslist.append(numworkers)
            for _ in xrange(numworkers):
                t = threading.Thread(target=worker, args=[
                    func, self.queues[i], self.queues[i+1]
                ])
                #t.daemon = True  # unnecessary
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

    def stop (self):
        """ Stop the whole pools chain.
        """
        for i in xrange(self.numpools):
            numworkers = self.numworkerslist[i]
            for j in xrange(numworkers):
                self.queues[i].put('__STOP__')
