#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 07:53:02 2018

@author: mohamed
"""

# =============================================================================
# This library could be imported via:
#   from k5descendants import LoneVertex as LV
# =============================================================================

#import graphs as g

#from sage.graphs.graph_generators import graphs
from sage.graphs.graph import Graph

from SimplePart import SimplePart

# =============================================================================
#
# =============================================================================

class LoneVertex(SimplePart):
    '''
    class LoneVertex.
    
        This is a class of non-triangle vertices, AKA lone vertices. The main list
            in this class is the vertices list and the chord_vector list, from
            which the other properties are calculated.
    
        For now, each LoneVertex instance should contain exactly one vertex. In the
            near future, as lone vertices are more understood, the class will be
            updated to reflect that.
    '''
    
    type = 'LoneVertex'      # class variable shared by all instances
    
    LoneVertex_version = 0.1
    

    def __init__(self, vertices=None, order=None, start_at=0, parent_object=None):
        '''
        Creates a LoneVertex object, which inherits from Part. 
        
        Options:
            vertices -          int or list -           Set the vertices to this list.
            order -             int -                   The number of vertices. Currently, only 1 is supported.
            start_at -          int -                   The label of the first vertex.
            parent_object       Pseudodescendant -      Set the parent_object to parent_object.      
        '''
               
        if vertices is None: 
            if order is None: order=1
            
            vertices=[start_at+i for i in range(0,order)]
    
        else:
            try:
                len(vertices)
            
            except TypeError:
                vertices=[vertices]
                
            
        self.vertices=vertices
        self.set_parent_object(parent_object)
        self.parts=[self]
        
    
    def triangles_count(self):
        '''
        Returns the number of triangles in self.
        '''
          
        return 0
    
    
    def graph(self, present_edges='full'):
        '''
        Returns Graph of self.
        '''
        
        return Graph([self.vertices,[]],format='vertices_and_edges')
    
    
    def chain_vector(self):
        '''
        Returns chain vector of self.
        '''
        
        return tuple([-self.order()])
    
    
    def reindex(self, start_at=0):
        '''
        Relabels the vertices, starting the label at start_at (default is 0).
        '''
        
        self.vertices=[start_at+i for i in range(0,self.order())]
        
        return max(self.vertices)
    
# =============================================================================
# Function is_isomorphic(self, vr2, use_optimizations=True):
#       VectorRepresentation, VectorRepresentation -> bool
#
# Checks if self and vr2 represent isomorphic graphs.
# =============================================================================