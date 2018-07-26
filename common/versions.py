#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 17:50:47 2018

@author: Mohamed Laradji
"""

# =============================================================================
# This module aims to contain the version information of k5-descendants modules.
# =============================================================================

from extended.eGraph import eGraph

def eGraph_version():
    return eGraph.version


from extended.eGraphIndexedSet import eGraphIndexedSet

def eGraphIndexedSet():
    return eGraphIndexedSet.version


import search.Family

def Family_version():
    return Family.version


from pseudodescendant.Pseudodescendant import Psuedodescendant

def Pseudodescendant_version()
    return Pseudodescendant.version