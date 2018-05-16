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

# =============================================================================
# function triangle_type(Type): integer -> Graph
# This function takes an integer 0<n<5 and outputs a "triangle" of the corresponding
#   type. See Figure 4.10 (Page 38-9) of thesis. The triangle to be expanded is
# [0,1,2] with 1 the special vertex.
# =============================================================================

def triangle_type(Type):
    
    if Type==1:
        return Graph([[0,1],[0,2],[1,2],[0,3],[2,3],[1,4],[1,5],[4,5]])
    elif Type==2:
        return Graph([[0,1],[0,2],[1,2],[0,3],[2,3]])
    elif Type==3:
        return Graph([[0,1],[0,2],[1,2],[1,3],[1,4],[3,4]])
    elif Type==4:
        return Graph([[0,1],[0,2],[1,2]])
    else:
        raise ValueError('Argument of triangle_type(Type) must be an integer 0<n<5.')