#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 11:19:42 2018

@author: mohamed
"""

# =============================================================================
# This library could be imported via:
#   from k5descendants import chainlist as cl
# =============================================================================

import common.graphs as g
#from common import exceptions

from copy import copy
#import itertools as itertools

from Zigzag import Zigzag
from Chain import Chain
from LoneVertex import LoneVertex



# =============================================================================
# Function list_zigzags(G): Graph -> list
#
#   This function produces a list of zigzags (list of vertices) in the graph G.
#       If G has multiple edges, the multiple edges are first removed.
#
#   Example: list_zigzags(g.
# =============================================================================

def make_zigzags(G):
    K=copy(G)
    
    K.allow_multiple_edges(0) 
    # Necessary as subgraph_search_iterator cannot yet handle multiple edges.

    triangles_count=K.triangles_count()
    max_triangles_count=triangles_count
    zigzag_list=[]
    
    while triangles_count>0:
        for i in range(max_triangles_count,0,-1):
            
            H=g.zigzag(i)
            H.allow_multiple_edges(0) 
            # Necessary as subgraph_search_iterator cannot yet handle multiple edges.
            
            
            try:
                zigzag=K.subgraph_search_iterator(H).next()
                zigzag_list.append(zigzag)
                
                K.delete_edges(K.subgraph(zigzag).edges())
                # This is so that the loops terminate.
                
                triangles_count=K.triangles_count()
                
                max_triangles_count=triangles_count
                
                break
            except StopIteration: continue
        
    Zigzags=[Zigzag(vertices=zigzag_vertices) for zigzag_vertices in iter(zigzag_list)]
        
    return Zigzags


#==============================================================================
# make_chains(Zigzags): list of Zigzag objects -> list of Chain objects 
#==============================================================================
    

def make_chains(zigzags):
    
    chain_list=[]
    
    zigzags=copy(zigzags)
    
    while len(zigzags)>0:

        chain=Chain(zigzag=zigzags.pop())
        
        for zigzag in iter(zigzags):
            try:
                chain.append_zigzag(zigzag)
                zigzags.remove(zigzag)
                
            except CannotAppendZigzag: continue
        
        chain_list.append(chain)
        
    return chain_list


#==============================================================================
# make_lone_vertices(G): Graph -> list of LoneVertex objects
#==============================================================================
    
def make_lone_vertices(graph):
       
    # .cluster_triangles() is not defined for multigraphs, but we sometimes deal
    #       with multigraphs. Thus, we will disallow multiple edges (on a copy).
    #   If a vertex v is part of a triangle in G, it must be part of a triangle
    #       in the underlying simple graph.
    
    
    G=copy(graph)
    G.allow_multiple_edges(0)
    
    cluster_triangles=G.cluster_triangles()
    
    lone_vertex_list=[]
    
    for vertex in cluster_triangles:
        if cluster_triangles[vertex]==0:
            lone_vertex=LoneVertex(vertex)
            lone_vertex_list.append(lone_vertex)
        
    return lone_vertex_list

#==============================================================================
# make_parts(G): Graph -> list of part objects (ie. LoneVertex or Chain)
#==============================================================================
    
def make_parts(graph):
    
    G=copy(graph)
    
    parts=make_chains(make_zigzags(G))
    
    lone_vertices=make_lone_vertices(G)
    
    parts.extend(lone_vertices)
    
    return parts