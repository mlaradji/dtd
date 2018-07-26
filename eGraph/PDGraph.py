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

#import copy
#import collections

# imports from sage
#from sage.graphs.graph import Graph
#from sage.graphs.graph_generators import graphs

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

from DTEGraph import DTEGraph

# =============================================================================
# Class definitions 
# =============================================================================


class PDGraph(DTEGraph):
    '''
    Pseudodescendant eGraph.
    
    This is an extension of the DTEGraph class. It adds functions particular to $K_5$-descendants and pseudo-descendants.
    '''
    
    def __init__(self, data = None, family = None, **kwargs):
        '''
        Can be initialized the same way as a sage Graph object.
        '''
        
        super(PDGraph, self).__init__(data, family = family, **kwargs)
        
        if not family is None: 
            self.count_functions['expanded_triangle_types'] = lambda G: family.expanded_triangle_types[G]
        
# =============================================================================
# Double triangle expansion (DTE)
# =============================================================================


    def DTE_edge_pairs_iterator(self, desired_expanded_triangle_types = [1,1,1,1]):
        '''
        Calculates and returns an iterator over the children of self.
        
        Options:
            desired_triangle_types_expanded -   list -      Only expand the triangle types indicated.
        '''
        
        #children=Family()
        
        
        return iter(self.triangles_by_type(desired_triangle_types = desired_expanded_triangle_types, output_edges = True))
        
    
# =============================================================================  
# Triangle types
# ============================================================================= 
    
    
    def triangles_by_type(self, desired_triangle_types=None, output_edges=False, disregard_edge_pair_order=True):
        '''
        function self.triangles_by_type: Graph -> list of 4 sets
        
        triangles_by_type finds all triangles in G and partitions them according to the "Triangle Type". 
    
        This function partitions triangles in G by their triangle type (wrt double triangle expansion),
            by iteratively searching the graph G for triangles that are not of the previous types. For example,
            to check that a triangle T is of type II, we need to check that it is isomorphic to the graph
            triangle_type(2) (which means the triangle is either Type I or Type II) but not to the graph   
            triangle_type(1).
            
        Options:
            output_edges -                  bool -  Default: False. If True, returns the special edges which would be subdivided in a double triangle expansion. If both outout_edges and disregard_edge_pair_order are True, it can result in an eight-fold speed-up, as each edge pair will appear only once instead of the eight times when both options are false.
            disregard_edge_pair_order -     bool -  Default: True. If True, disregards the order of the edges, which is inconsequential in a double triangle expansion since both those edges will be subdivided. This option is only considered when output_edges=True.
        '''
        
        ValueError_count = 0
        ValueError_threshold = 2
        
        H = self.copy(immutable = False)
        
        while ValueError_count < ValueError_threshold:
            try:
                triangles_by_type=[set(),set(),set(),set()]

                for i in range(0,4):

                    #if not triangles_by_type[i]: continue

                    for triangle in H.subgraph_search_iterator(g.triangle_type(i+1, with_adjacent_edge=True)):

                        triangle=triangle[0:4]      # The first four vertices are always the same.

                        if output_edges: 
                            edge1=(triangle[0],triangle[2])
                            edge2=(triangle[1],triangle[3])

                            if disregard_edge_pair_order:
                                edge1=tuple(sorted(edge1))
                                edge2=tuple(sorted(edge2))
                                edge1, edge2 = min(edge1,edge2), max(edge1,edge2)

                            triangle=[edge1, edge2]

                        triangle=tuple(triangle)

                        good_to_add=True

                        for j in range(0,i):
                            if triangle in triangles_by_type[j]: 
                                good_to_add = False
                                break

                        if good_to_add: triangles_by_type[i].add(triangle)

                if desired_triangle_types is None:
                    return triangles_by_type

                else:
                    combined_triangles_set=set()
                    for i in range(0,4):
                        if desired_triangle_types[i]: 
                            combined_triangles_set=combined_triangles_set.union(triangles_by_type[i])

                    return combined_triangles_set
                
            except ValueError:

                ValueError_count+=1

            # These lines are to avoid the multigraph error in subgraph_search_iterator.
                H.allow_multiple_edges(False)
                H.allow_loops(False)

                continue
    
    
    
# =============================================================================
#   Standalone functions
# =============================================================================

# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 
