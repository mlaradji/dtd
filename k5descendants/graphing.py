#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon June  22 13:10:28 2018

@author: mohamed
"""

# =============================================================================
# This library could be imported via:
#   from k5descendants import graphing as gr
# =============================================================================


import dtrl as dtrl
import vpdl as vpdl
import examples as examples
import chord_order as co

import time as time
import pickle as pickle
import itertools as itertools
from collections import OrderedDict as OrderedDict

from copy import deepcopy

from sage.graphs.graph import Graph
from sage.graphs.graph_generators import graphs
from sage.rings.finite_rings.integer_mod import mod


# =============================================================================
# Function graph_form(vector): list -> graph
#
#   This function converts a vector representation - a chain vector and a chor-
#       -d length vector - into a graph object.
# =============================================================================

def graph_form(chain_vector,chord_length_vector):
    
    G, chain_vertices_list=skeleton(chain_vector, output_chain_vertices_list=True)
    chord_edges=make_chord_edges_list(chain_vertices_list, chord_length_vector)
    
    G.add_edges(chord_edges)
    
    return G    
    

# =============================================================================
# Function make_chord_edges_list(chain_vertices_list, chord_length_vector): 
#       list, list -> list
#
#   This function takes a chord length vector and a dictionary of positions and
#       outputs a list of chord edges. Note that this function assumes that it 
#       is not an n-zigzag.
#
#   Example:    import k5descendants.graphing as gr
#               ch,clv=(2,0,-1,0,-1,0,2,0),(4,6,4,7,1,4,1,4,1,4)
#               cvl=gr.make_chain_vertices_list(ch)
#               H=gr.skeleton(ch)
#               pos=vt.vertex_positions(H,cvl) 
#               cvl
#               >>> [[[0, 1, 2, 3]], [[4]], [[5]], [[6, 7, 8, 9]]]
#               pos
#               >>> {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9]}
#               gr.make_chord_edges_list(pos,clv)
#               >>> [(0, 4), (0, 6), (1, 5), (2, 9), (3, 4), (3, 7), (4, 5), (4, 8), (5, 6), (5, 9)]
#               
# =============================================================================

def make_chord_edges_list(chain_vertices_list, chord_length_vector, verbose=0):
    
    clv=iter(chord_length_vector)
    chord_vertices_list, degree=make_chord_vertices_list(chain_vertices_list)
    chord_edges_list=[]
    edge_index=0
    
    for i in range(0,len(chord_vertices_list)):

        v1=chord_vertices_list[i]
            
        while degree[v1]<4:
            
            v2=chord_vertices_list[i+clv.next()]
            
            chord_edges_list.append((v1, v2))
            degree[v1]+=1
            degree[v2]+=1
            
            if verbose: print(degree)
                
    return chord_edges_list


# =============================================================================
# function make_chord_vertices_list(chain_vertices_list): list -> list
#   
#   This function takes a chain vertices list and produces an ordered list of
#       chord vertices. Note that this function assumes that it is not an n-zigzag.
#
#   Example:    make_chord_vertices_list([[[1, 5, 8, 7]], [[2, 4, 9, 3]], [[0]], [[6]]])
#               >>> [1, 5, 8, 7, 2, 4, 9, 3, 0, 6], {0: 4, 1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 4, 7: 2, 8: 3, 9: 3}                                          
#
#   Example:    make_chord_vertices_list([[[0,1,2,3],[3,4,5,6,7,8]],[[9]],[[10,11,12]]])
#               >>> ([0, 1, 2, 4, 7, 8, 9, 10, 11, 12], 
#                       {0: 2, 1: 3, 2: 3, 4: 3, 7: 3, 8: 2, 9: 4, 10: 2, 11: 2, 12: 2})
# =============================================================================

def make_chord_vertices_list(chain_vertices_list):

    chord_vertices_list=[]
    degree=dict()
    
    for chain in iter(chain_vertices_list):
        
        c=len(chain)
        
        for i in range(0,c):
            z=len(chain[i])
            if z<3:
                chord_vertices_list.append(chain[i][0])
                degree[chain[i][0]]=0
                break
            else:
                if i==0:
                    chord_vertices_list.append(chain[i][0])
                    degree[chain[i][0]]=2
                    
                
                if z>3:
                    chord_vertices_list.append(chain[i][1])
                    chord_vertices_list.append(chain[i][-2])
                    degree[chain[i][1]]=3
                    degree[chain[i][-2]]=3
                elif z==3:
                    chord_vertices_list.append(chain[i][1])
                    degree[chain[i][1]]=2
                if i==c-1:
                    chord_vertices_list.append(chain[i][-1])
                    degree[chain[i][-1]]=2
                
    return chord_vertices_list, degree


# =============================================================================
# Function skeleton(chain_vector): list -> graph
#
#   This function takes a chain vector and outputs a graph skeleton that consi-
#       sts of chain and zigzag parts and no chord edges.
# =============================================================================

def skeleton(chain_vector, output_chain_vertices_list=False, verbose=0):
    
    G=Graph()
    
    chain_vertices_list=make_chain_vertices_list(chain_vector)
    if verbose: print(chain_vertices_list)
    
    for chain in iter(chain_vertices_list):
        
        if verbose>1: print('chain: '+str(chain))
            
        for zigzag in iter(chain):
              
            if len(zigzag)>2:  # This indicates it is at least a triangle.
                make_zigzag(G,zigzag)
                
            else:
                for vertex in iter(zigzag):
                    G.add_vertex(vertex)
                
            if verbose>2: print('zigzag: '+str(zigzag))
            if verbose>3: 
                print('edges: '+str(G.edges()))
                print('vertices: '+str(G.vertices()))
    
    if output_chain_vertices_list:
        return G, chain_vertices_list
    else:
        return G


# =============================================================================
# Function make_chain_vertices_list(chain_vector): list -> list
#
#   This function takes a chain vector and outputs a chain_vertices_list that
#       can be used to create the graph represented by that chain vector.
#
#   Example:    cv=(2,0,-1,0,-1,0,2,0)
#               chain_vertices_list(cv)
#               >>> [[[0, 1, 2, 3]], [[4]], [[5]], [[6, 7, 8, 9]]]
#
#   Example:    cv=(2,2,0,-1,0)
#               chain_vertices_list(cv)
#               >>> [[[0, 1, 2, 3],[3, 4, 5, 6]], [[7]]]
# =============================================================================

def make_chain_vertices_list(chain_vector,verbose=0):
    
    vertex_index=-1
    chain_vertices=[]
    same_chain=0
    
    for zigzag in iter(chain_vector):
 
        if zigzag>0:
            
            zigzag_vertices=[]
            
            if same_chain:
                zigzag_vertices.append(vertex_index)
                
            else:
                vertex_index+=1
                zigzag_vertices.append(vertex_index)
                
            for i in range(1,zigzag+2):
                vertex_index+=1
                zigzag_vertices.append(vertex_index)
            
            if same_chain:
                chain_vertices[-1].append(zigzag_vertices)
        
            else:
                chain_vertices.append([zigzag_vertices])
                
            same_chain=1
        
        elif zigzag==0:
            same_chain=0
        
        elif zigzag==-1:
            vertex_index+=1
            chain_vertices.append([[vertex_index]])
            same_chain=0    # This line might not be necessary.
        
        else:
            raise ValueError('Dealing with values less than -1 in the chain vector has not been implemented.')
        
        if verbose: print(zigzag_vertices)
        
    return chain_vertices
    

# =============================================================================
# Function make_zigzag(G, vertex_list): graph, list -> None
#
#   This function takes a vertex_list and a graph G, and adds vertices and edg-
#       -es of G so that vertex_list is the ordered list of a zigzag subgraph 
#       of G. Note that this function changes G.
#
#   Example:    G=Graph()
#               v=[0,1,2,3,4,5]
#               make_zigzag(G,v)
#               G.is_isomorphic(examples.zigzag(4))
#               >>> True
#
# =============================================================================

def make_zigzag(G, vertex_list):
    
    for i in range(0,len(vertex_list)):
        G.add_vertex(vertex_list[i])
        
        if i>0: G.add_edge(vertex_list[i],vertex_list[i-1])
        if i>1: G.add_edge(vertex_list[i],vertex_list[i-2])
        
    return


# =============================================================================
# 
#
# =============================================================================