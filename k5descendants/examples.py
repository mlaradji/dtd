#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:24:47 2018

@author: mohamed
"""

from sage.graphs.graph import Graph

# =============================================================================
# 
# =============================================================================

def zigzag(n):
    
#The output of this function is the zigzag graph (not 4-regular) with n+2 vertices, Z*n.
    
    G=Graph()
    G.add_vertices([i for i in range(0,n+2)])
    G.add_edges([i,(i+1)%(n+2)] for i in range(0,n+1))
    G.add_edges([i,(i+2)%(n+2)] for i in range(0,n))
    return G


def one_zigzag(n):
    
#The output of this function is the 1-zigzag graph (4-regular) with n+2 vertices, Zn.
    
    G=Graph()
    G.add_vertices([i for i in range(0,n+2)])
    G.add_edges([i,(i+1)%(n+2)] for i in range(0,n+2))
    G.add_edges([i,(i+2)%(n+2)] for i in range(0,n+2))
    return G

#def n_zigzag_skeleton(n):

#def triangle_type

def triangle():
    return Graph([(0,1),(0,2),(1,2)])

        
# =============================================================================
#
# =============================================================================