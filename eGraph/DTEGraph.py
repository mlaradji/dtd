#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  22 15:53:21 2018

@author: Mohamed Laradji
"""

# =============================================================================
# Import statements 
# =============================================================================

# Add location to search for imports

#sys.path.append('..')  # This seems to be unnecessary. Unsure why.

# imports 

import copy
#import collections

# imports from sage
from sage.graphs.graph import Graph
from sage.graphs.graph_generators import graphs

# imports from thirdparty

#try:
#    from boltons import setutils  # Note that this requires to be installed.

#except ImportError:
#    from thirdparty.boltons import setutils

# imports from common
import common.graphs as g
#import common.functions as f
#from common.exceptions import NotSubgraph, Underdefined
#from common.exceptions import UnsupportedOption

# object imports

#from search.Family import Family

from eGraph import eGraph
from eGraphSet.eGraphSet import eGraphSet

# =============================================================================
# Class definitions 
# =============================================================================


class DTEGraph(eGraph):
    '''
    Double Triangle Expandable eGraph.
    
    This is an extension of the eGraph class. It adds functions related to double triangle expansion to the class. This class aims to contain functions related to double triangle expansion but not particular to $K_5$-descendants. For the special $K_5$-descendants class, see PDGraph.
    '''
    
    
    def __init__(self, data = None, family = None, **kwargs):
        '''
        Can be initialized the same way as a sage Graph object.
        '''
        
        super(DTEGraph, self).__init__(data, **kwargs)
        
        self.family = family
        
        self.count_functions['expanded'] = lambda G: not self.family is None and self.family.expanded[G]
            
            
                
# =============================================================================

    def copy(self, **kwargs):
        '''
        Copies the DTEGraph object. Makes sure that the hashes, counts, and count_functions are also copied.
        '''
        
        graph = super(DTEGraph, self).copy(**kwargs)
        
        graph.hashes, graph.counts, graph.count_functions = self.hashes, self.counts, self.count_functions
        
        graph.family = self.family
        
        return graph
        
        
# =============================================================================
# Double triangle expansion (DTE)
# =============================================================================

    def DTE(self, *pargs, **kwargs):
        '''
        Alias for double_triangle_expansion.
        '''
        
        return self.double_triangle_expansion(*pargs, **kwargs)

    
# =============================================================================


    def DTR(self, *pargs, **kwargs):
        '''
        Alias for double_triangle_reduction.
        '''
        
        return self.double_triangle_reduction(*pargs, **kwargs)
    
    
# =============================================================================


    def children(self, **kwargs):
        '''
        Calculates and returns a set of all children of self. Same kwargs as self.children_iterator.
        '''
        
        return set(self.children_iterator(**kwargs))
    
 # =============================================================================   

    def children_iterator(self, only_nonisomorphic = False, **kwargs):
        '''
        Calculates and returns an iterator over the children of self.
        
        Options:
            only_nonisomorphic -    bool -      If False, returns all labeled children. If true, removes isomorphic copies.
            
            edge_pair_provider -    function -  Expects a function that takes a graph as input. This option can be used to only expand certain triangles of self.
        '''
            
        DTE_edge_pairs = self.DTE_edge_pairs_iterator(**kwargs)
        
        children = eGraphSet()
            
        for edge_pair in DTE_edge_pairs:
            
            #try:
                
            child = self.double_triangle_expansion(edge_pair[0], edge_pair[1], new_graph = True)
            
            duplicate_graph = None
            
            duplicate_graph = children.add_graph(child, require_nonisomorphic = only_nonisomorphic)
                
            if duplicate_graph is None: yield child
                

# =============================================================================

    def DTE_edge_pairs_iterator(self):
        '''
        Returns an iterator over the edge pairs of triangle and edges in self. Meant to be used with self.children.
        '''
        
        return self.triangle_and_edge_iterator(return_edges = True)
    
# =============================================================================


    def double_triangle_expansion(self, e1 = None, e2 = None, check_if_DTE = True, new_graph = True):
        '''
        Subdivides e1, e2 and identifies the resultant degree 2 vertices. Returns the new vertex that was created.
        
        If e1 (or e2) is an edge in a triangle T, and e2 (or e1) is an edge not in T adjacent to the vertex in T opposite to e1 (or e2), then this operation is called a double triangle expansion (DTE).
        
        Options:
            check_if_DTE -  bool -  Default: True. If True, raises an InvalidDTE exception if the DTE is not valid.
            
            new_graph -     bool -  Default: True. If True, creates a new eGraph object and leaves self unchanged.
        '''
        
        if e1 is None and e2 is None:
            e1, e2 = self.DTE_edge_pairs_iterator().next()
    
        if check_if_DTE:
            
            if self.is_triangle_and_edge(e1,e2): pass
            
            else: 
                raise InvalidDTE('e1, e2 are not edges of a triangle and edge (Tadpole(3,1)) subgraph of '+str(self)+'.')
                
        if new_graph:
            child = self.copy(immutable = False)
            
        else:
            child = self
            
        child.crossing_into_vertex(e1, e2)
        
        return child
    
    
# =============================================================================
    
    def double_triangle_iterator(self, not_triple_triangle = True):
        '''
        Returns an iterator over the double triangles of self. If not_triple_triangle is True, it will remove the double triangles that are also part of triple triangles.
        '''

        
        if not_triple_triangle:
            triple_triangles = set()
            for triple_triangle in self.subgraph_search_iterator(g.triple_triangle()):
                triple_triangles.add(tuple(triple_triangle[0:4]))
        
        for double_triangle in self.subgraph_search_iterator(g.double_triangle()):
            double_triangle = tuple(double_triangle)
            
            if not_triple_triangle and double_triangle in triple_triangles: continue
                
            yield double_triangle
    
# =============================================================================

    def double_triangle_reduction(self, double_triangle = None, new_graph = True):
        '''
        Reduces the indicated double triangle. double_triangle expected to be a 4-tuple of vertices, with positions 0 and 2 the vertices of the common edge between the two triangles. This does not check if the double_triangle is part of a triple triangle, but that will probably be implemented quite soon.
        '''
        
        if double_triangle is None:
            try:
                double_triangle = self.double_triangle_iterator().next()
                
            except StopIteration:
                raise NoProperDoubleTriangles('self does not have any double triangles that are part of triple triangles.')
            
        v0, v1, v2, v3 = double_triangle
        
        if new_graph: parent = self.copy(immutable = False)
        else: parent = self
            
        parent.delete_edges([(v0,v2),(v1,v2),(v3,v2)])
        parent.add_edge(v1,v3)
        parent.identify_vertices(v0,v2)
        
        return parent
    
# =============================================================================

    def ancestor(self, no_triple_triangles = True):
        '''
        Iteratively reduces all double triangles that are not triple triangles until unable to do so. For a K5-descendant, this should return K5.
        
        Options:
            no_triple_triangles -   bool -  Not Implemented Yet! Default: True. If False, reduces all double triangles regardless if they are part of triple triangles. Note that reducing a triple triangle creates multiple edges, which may not  be enabled by default. To get the right graph, call self.allow_multiple_edges(1) first before self.ancestor(options).
        '''
        
        graph = self.copy(immutable = False)
        
        while True:
            try:
                double_triangle = graph.double_triangle_iterator(not_triple_triangle = no_triple_triangles).next()
                graph.double_triangle_reduction(double_triangle, new_graph = False)
                
            except StopIteration:
                break
        
        return graph

# =============================================================================


    #def parents_iterator(self):
        
# ============================================================================= 
#   Triangle and Edge (AKA Tadpole(3,1))
# ============================================================================= 

    def is_triangle_and_edge(self,e1=None,e2=None, also_reverse_e2=True, also_reverse_e1_e2=True):
        '''
        If e1 and e2 are specified, returns True if e1, e2 are part of a triangle and edge (AKA Tadpole(3,1)), and False otherwise. If e1 and e2 are unspecified, returns self.is_isomorphic(g.triangle_and_edge()).  
        '''
        
        e1 = copy.copy(e1)
        e2 = copy.copy(e2)
        
        if e1 is None and e2 is None:
            return self.is_isomorphic(g.triangle_and_edge())
        
        condition=g.triangle_and_edge(e1,e2).is_subgraph(self, induced=False)
        
        if condition: return True
        
        elif also_reverse_e2:
            e2=(e2[1],e2[0])
            return self.is_triangle_and_edge(e1, e2, also_reverse_e2=False, also_reverse_e1_e2=also_reverse_e1_e2)
        
        elif also_reverse_e1_e2:
            return self.is_triangle_and_edge(e2, e1, also_reverse_e2=True, also_reverse_e1_e2=False)
        
        else:
            return False
        
# =============================================================================        
        
    def triangle_and_edge_iterator(self, return_edges=False):
        '''
        If return_edges=True, this returns an iterator of tuples of the edges. If False, which is the default, it returns an iterator over the vertex sets of the subgraphs.
        
        The vertex sets are ordered. e1=[0,2] (triangle_edge), e2=[1,3] (path_edge)
        '''
        
        G=copy.deepcopy(self)
        G.allow_multiple_edges(0) # This is done because self.subgraph_search_iterator does not yet work with multigraphs.
        
        iterator=self.subgraph_search_iterator(g.triangle_and_edge())
        while True:
            if return_edges:
                yield get_edge_triangle_and_edge(iterator.next())
            
            else:
                yield iterator.next()
     

# =============================================================================
# Graph isomorphism
# =============================================================================
         
    def has_K4(self):
        '''
        Returns True if self has a subgraph isomorphic to K_4, and False otherwise.
        '''
        
        K4=graphs.CompleteGraph(4)
        return self.has_isomorphic_subgraph(K4)

# =============================================================================   
        
    def has_T3(self):
        '''
        Returns True if self has a subgraph isomorphic to T^3 (triple triangle), and False otherwise.
        '''
        
        T3=Graph([(0,1),(0,2),(1,2),(0,3),(2,3),(0,4),(2,4)])
        return self.has_isomorphic_subgraph(T3)
       
# =============================================================================
#   Standalone functions
# =============================================================================

def get_edge_triangle_and_edge(vertices):
    e1=(vertices[0],vertices[2])    # opposite triangle edge
    e2=(vertices[1],vertices[3])    # edge
    e3=(vertices[0],vertices[1])    # triangle edge
    e4=(vertices[1],vertices[2])    # triangle edge
    return e1,e2,e3,e4
    
    
# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 

class InvalidDTE(Exception):
    '''
    Raised when the requested double triangle expansion is invalid.
    '''
    
    pass

# =============================================================================

class InvalidDTR(Exception):
    '''
    Raised when the requestion double triangle reduction is invalid.
    '''
    
    pass

# =============================================================================

class NoProperDoubleTriangles(Exception):
    '''
    Raised when a graph has no double triangles that are not part of triple triangles.
    '''
    
    pass