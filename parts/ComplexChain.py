#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 17:14:04 2018

@author: mohamed
"""

# =============================================================================
# This library could be imported via:
#   from k5descendants import Chain as C
# =============================================================================

from sage.graphs.graph import Graph

from Zigzag import *
from ChordVector import *
from Chain import *

from common.exceptions import *

import convert_Graph_to_Pseudodescendant as cgpd

#import vector_representation as vrep

from collections import OrderedDict as OrderedDict
from copy import copy


# =============================================================================
# class ComplexChain
# =============================================================================

class ComplexChain(Chain):
    
        pass