#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:24:47 2018

@author: Mohamed Laradji
"""

from sage.graphs.graph import Graph
from sage.graphs.graph_generators import graphs

# =============================================================================
# 
# =============================================================================

def zigzag(n, vertices=None):
    '''
    The output of this function is the zigzag graph (not 4-regular) with n+2 vertices, $Z^*_n$.
    '''
    
    G=Graph()
    G.allow_multiple_edges(1)
    G.add_vertices([i for i in range(0,n+2)])
    G.add_edges([i,(i+1)%(n+2)] for i in range(0,n+1))
    G.add_edges([i,(i+2)%(n+2)] for i in range(0,n))
       
    if vertices==None:
        return G
    
    elif len(vertices)==n+2:
        labels=dict()
        for i in range(0,n+2):
            labels[i]=vertices[i]
        
        G.relabel(labels)
        return G
    
    else: raise ValueError('The list ''vertices'' needs to be of length n.')
        
        
def Zstar(*pargs, **kwargs):
    '''
    Shorthand for zigzag.
    '''
    
    return zigzag(*pargs, **kwargs)      


def one_zigzag(n):
    '''
    The output of this function is the 1-zigzag graph (4-regular) with n+2 vertices, $Z_n$.
    '''

    G=Graph()
    G.allow_multiple_edges(1)
    G.add_vertices([i for i in range(0,n+2)])
    G.add_edges([i,(i+1)%(n+2)] for i in range(0,n+2))
    G.add_edges([i,(i+2)%(n+2)] for i in range(0,n+2))
    return G

def Z(*pargs, **kwargs):
    '''
    Shorthand for one_zigzag.
    '''
    
    return one_zigzag(*pargs, **kwargs)


def K5():
    '''
    Returns the complete graph $K_5$.
    '''
    
    return graphs.CompleteGraph(5)


def triple_triangle():
    '''
    Returns a triple triangle.
    '''
    
    triangle_1 = [(0,1),(0,2),(1,2)]
    triangle_2 = [(0,2),(0,3),(2,3)]
    triangle_3 = [(0,2),(0,4),(2,4)]
    
    edges = set(triangle_1).union(triangle_2).union(triangle_3)
    triple_triangle = Graph(list(edges))
    
    return triple_triangle


def double_triangle():
    '''
    Returns a double triangle.
    '''
    
    triangle_1 = [(0,1),(0,2),(1,2)]
    triangle_2 = [(0,2),(0,3),(2,3)]
    
    edges = set(triangle_1).union(triangle_2)
    double_triangle = Graph(list(edges))
    
    return double_triangle
        
# =============================================================================
#
# =============================================================================

# 

    

def triangles_count_Z(n):
    '''
    This is faster to calculate than g.triangles_count(g.one_zigzag(n)).
    '''

    if n==1 or n==2:
        return 8
    elif n==3:
        return 10
    elif n==4:
        return 8
    elif n>=5:
        return n+2
    
def order_Z(n): 
    '''
    Returns the order of $Z_n$.
    '''
    
    return n+2

def is_one_zigzag(G):
    '''
    Returns True if G is a 1-zigzag, and returns False otherwise.
    ''' 
    
    n=G.order()
    if G.is_isomorphic(one_zigzag(n-2)): return n-2
    else: return 0


def is_zigzag(G):
    '''
    Returns True if G is a zigzag, and returns False otherwise.    
    '''
    
    n=G.order()
    if G.is_isomorphic(zigzag(n-2)): return n-2
    else: return 0
    
    
    
# =============================================================================
# Function get_graph(graph): supported_type or Graph -> Graph
#
#   If graph is in supported_types, this function returns graph.graph(), and if
#       graph is a Graph object, it returns graph (ie itself).
# =============================================================================
        

def get_graph(graph):
    '''
    Function get_graph(graph): supported_type or Graph -> Graph
    
    If graph is in supported_types, this function returns graph.graph(), and if graph is a Graph object, it returns graph (ie itself).
    '''
    
    supported_types={'Pseudodescendant', 'Chain', 'Zigzag', 'LoneVertex'}
    
    try:
        if graph.type in supported_types:
            G=graph.graph()
        
    except AttributeError:        
        if type(graph) is Graph:
            G=graph
            
        else:
            raise TypeError('graph must of type Graph or of a type in '+str(supported_types)+'.')
                
    return G


def triangle_and_edge(e1=None, e2=None, reverse_e2=False):
    '''
    Returns a triangle and edge graph, which is isomorphic to sage.graphs.Tadpole(3,1).
    '''
    
    triangle_and_edge=graphs.CycleGraph(3)
    triangle_and_edge.add_edge(1,3)
    
    label={i:i for i in range(0,3)}
    
    if not e1 is None:
        label[0]=e1[0]
        label[2]=e1[1]
        
    if not e2 is None:
        if reverse_e2:
            label[1]=e2[1]
            label[3]=e2[0]
        else:
            label[1]=e2[0]
            label[3]=e2[1]            
        
    triangle_and_edge.relabel(label)
        
    return triangle_and_edge


def triangle_type(Type, with_adjacent_edge=False):
    '''
    function triangle_type(Type): integer -> Graph

    This function takes an integer 0<n<5 and outputs a "triangle" of the corresponding
        type. See Figure 4.10 (Page 38-9) of Double Triangle Descendants of K5 (thesis). The triangle to be expanded        
        is [0,1,2] with 1 the special vertex.
    '''
    
    
    if Type==1:
        return triangle(with_base_triangle=True, with_adjacent_edge=with_adjacent_edge, with_opposite_triangle=True, with_adjacent_triangle=True)
    
    elif Type==2:
        return triangle(with_base_triangle=True, with_adjacent_edge=with_adjacent_edge, with_opposite_triangle=False, with_adjacent_triangle=True)
    
    elif Type==3:
        return triangle(with_base_triangle=True, with_adjacent_edge=with_adjacent_edge, with_opposite_triangle=True, with_adjacent_triangle=False)
    
    elif Type==4:
        return triangle(with_base_triangle=True, with_adjacent_edge=with_adjacent_edge, with_opposite_triangle=False, with_adjacent_triangle=False)
    
    else:
        raise ValueError('Argument of triangle_type(Type) must be an integer 0<n<5.')
        
        
def triangle(with_base_triangle=True, with_adjacent_edge=False, with_opposite_triangle=False, with_adjacent_triangle=False):
    '''
    Returns a Graph object (a triangle) according to the options. This is related to double triangle expansion triangle types. The special edges are always (0,2), the base triangle edge, and (1,3), the edge not in the base triangle but adjacent to the vertex (vertex 1) opposite to (0,2) that is in the base triangle.
    
    Options:
        with_base_triangle -        bool - Default: True.
                                            Whether to include the main triangle.
        with_adjacent_edge -        bool - Default: False.
                                            Whether to include the edge adjacent to but not in the base triangle.
        with_opposite_triangle -    bool - Default: False.
                                            Whether to include a triangle containing the adjacent_edge.
        with_adjacent_triangle -    bool - Default: False.
                                            Whether to include a triangle sharing an edge with the base_triangle.
    '''
    
    edges=set()
    
    if with_base_triangle:
        base_triangle=set([(0,1),(0,2),(1,2)])
        edges=edges.union(base_triangle)
    
    if with_adjacent_edge:
        adjacent_edge=set([(1,3)])
        edges=edges.union(adjacent_edge)
        
    if with_opposite_triangle:
        opposite_triangle=set([(1,3),(1,4),(3,4)])
        edges=edges.union(opposite_triangle)
    
    if with_adjacent_triangle:
        adjacent_triangle=set([(0,5),(2,5)])
        edges=edges.union(adjacent_triangle)
        
    return Graph(list(edges))