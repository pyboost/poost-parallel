# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 06/24/2013, updated 07/19/2013
#
""" Helper functions and templates for parallel computing.
"""

from __future__ import absolute_import

print('Executing %s' %  __file__)

import sys
if not (2, 6) <= sys.version_info < (3, ):
    raise ImportError("CPython 2.6.x or 2.7.x is required (%d.%d detected)."
                      % sys.version_info[:2])


from .multiproc import *
from .multithread import *


del sys, absolute_import

__version__ = '0.13.2-a3'
