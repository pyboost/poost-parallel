#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 06/24/2013, updated 07/01/2013
#
""" Helper functions and templates for multiprocessing.

    http://docs.python.org/2/library/multiprocessing.html#examples
    http://hg.python.org/cpython/file/3.3/Lib/concurrent/futures/process.py
"""
__all__ = [
    'ProcessPoolsChain',
]
print('Executing %s' %  __file__)

import os, sys, time
from multiprocessing import Manager, Process, Pool, Pipe, Queue


def worker (func, inque, outque):
    """ Worker process.
    """
    for index, item in iter(inque.get, '__STOP__'):
        # the 2nd form of iter:
        # the callable is called until it returns the sentinel
        output = func(item)
        outque.put((index, output))


class ProcessPoolsChain (object):
    """ Asynchronous worker-process pools chained by queues.
    """
    def __init__ (self, *funcs_workers):
        """ Constructor for ProcessPoolsChain.
            e.g. ProcessPoolsChain( (func1, num1), (func2, num2) )
            means num1 workers for func1, num2 for func2.
        """
        self.numpools = len(funcs_workers)
        self.numworkerslist = []
        self.queues = [Queue() for _ in xrange(self.numpools+1)]
        for i, (func, numworkers) in enumerate(funcs_workers):
            self.numworkerslist.append(numworkers)
            for _ in xrange(numworkers):
                Process(target=worker, args=(
                    func, self.queues[i], self.queues[i+1]
                )).start()
                print func, _

    def feed (self, inputs):
        """ Feeds a sequence of data into the (first) input queue, and obtains
            a sequence of outputs that match the input order.
        """
        numinputs = len(inputs)
        outputs = [None for _ in xrange(numinputs)]
        for index, item in enumerate(inputs):
            self.queues[0].put((index, item))

        # get results
        finished = set()
        while len(finished) < len(outputs):
            index, result = self.queues[-1].get()  # blocked
            outputs[index] = result
            finished.add(index)
        return outputs

    def stop (self):
        """ Stops the whole pools chain.
        """
        for i in xrange(self.numpools):
            numworkers = self.numworkerslist[i]
            for j in xrange(numworkers):
                self.queues[i].put('__STOP__')

