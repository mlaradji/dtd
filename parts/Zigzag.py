#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 07:53:02 2018

@author: mohamed
"""

# =============================================================================
# This library could be imported via:
#   from k5descendants import Zigzag as Z
# =============================================================================

import common.graphs as g
from common.exceptions import NotVertex

from SimplePart import SimplePart

#from boltons.setutils import IndexedSet

#from sage.graphs.graph_generators import graphs

# =============================================================================
#
# =============================================================================

class Zigzag(SimplePart):
    
    type = 'Zigzag'      # class variable shared by all instances

    def __init__(self, triangles_count=None, first_vertex=0, vertices=None, parent_object=None):
        
        '''
        Creates a Zigzag object, which inherits from Part. 
        
        Options:
            triangles_count -   int>0 -     The number of triangles in the zigzag.
            start_at -          int -       The label of the first vertex. This is only considered when triangles_count is set.
            vertices -          list -      Set the vertices to this list. They are assumed to be in zigzag ordering.
            parent_object       Chain -     Set the parent_object to Chain.      
        '''
        
        self.parts=[self]
        
        if triangles_count is None: 
            triangles_count=1
        
        elif triangles_count<1:
            raise ValueError('triangles_count must be >0. Received '+str(triangles_count)+' instead.')
        
        if vertices is None:
            vertices=[first_vertex+i for i in range(0,triangles_count+2)]
            
        self.vertices=vertices
        
        self.set_parent_object(parent_object)
        
        
#----------
# Vertices 
#----------
             

    def zigzag_vertices(self):
        '''
        Returns the vertices of self.
        '''
        
        return self.vertices
    
    
        
    def triangles_count(self):
        '''
        Returns the number of triangles in self.
        '''
        
        return self.order()-2
    
    
    def graph(self, present_edges=None):
        '''
        Returns a Graph object of self
        '''
        
        return g.zigzag(self.triangles_count(), vertices=self.vertices)
        # If triangles_count=0 it is an edge, and if triangles_count=-1, it is a lone vertex.
        
    
    def reverse(self): 
        '''
        This reverses the order of the vertices in self.
        '''
        
        self.vertices=list(reversed(self.vertices))

        
    def reindex(self, start_at=0, last_vertex=None):
        '''
        Relabels the vertices of self.
        
        Options:
            start_at -      int -   Start the vertex index at this value.
            last_vertex -   int -   Relabel the last vertex of self with this value.
                                        Note that last_vertex only affects the last vertex. For example, if 
                                        self.vertices=[0,1,2,3,4]. self.reindex(start_at=5, last_vertex=0) 
                                        will result in self.vertices=[5,6,7,8,0].
        '''
        
        end_at=start_at+self.order()-1
        if last_vertex is None: last_vertex=end_at
        
        self.vertices=[i for i in range(start_at,end_at+1)]
        self.vertices[-1]=last_vertex
             
        return last_vertex
    
    
    def make_first_vertex(self,vertex, make_last_vertex=False):
        '''
        # This function changes vertex to be the first vertex if it is possible,
        #   and returns True if it is possible and returns False if not.
        # With make_last_vertex=True, this function changes vertex to be the
        #   last vertex and return True if possible, and if not possible returns
        #   False.
        '''
        
        first_vertex, last_vertex=self.first_vertex(), self.last_vertex()
        
        if make_last_vertex:
            v=first_vertex
            first_vertex=last_vertex
            last_vertex=v
        
        order=self.order()
        
        if not self.is_end_vertex(vertex):
            raise CannotMakeFirstVertex('Vertex '+str(vertex)+' is not an end vertex.')
        
        if first_vertex==vertex: return True
        
        else:            
            if order>3:
                if last_vertex==vertex and self.is_end_vertex(first_vertex):
                    self.reverse()
                    return True
                
                else:
                    raise CannotMakeFirstVertex('Zigzag needs to be reversed but it can''t be')
            
            elif order<3:
                raise OrderLT3('Zigzag must have at least 3 vertices.')
                
            else:
                
                if self.is_end_vertex(first_vertex):
                    self.interchange_vertices(vertex,first_vertex)
                    return True
                else:
                    raise CannotMakeFirstVertex('The first vertex of zigzag is already fixed.')    
            
            
        raise ValueError('Unexpected error 1-923-9423.')
        
            
    def interchange_vertices(self,vertex1,vertex2):
        '''
        # This function interchanges the labelling of two vertices in the zigzag.
        #   Note that this function does not check if the interchanging is valid.
        '''
        
        if not (self.has_vertex(vertex1) and self.has_vertex(vertex2)):
            raise NotVertex('Both vertex1 and vertex2 must be in the zigzag.')
        
        relabel=dict()
        relabel[vertex1]=vertex2
        relabel[vertex2]=vertex1
        
        for vertex in iter(self.vertices):
            if vertex not in relabel: relabel[vertex]=vertex
                        
        self.vertices=[relabel[vertex] for vertex in iter(self.vertices)]        
        return
        
    
# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 

class CannotMakeFirstVertex(Exception):
    pass

class OrderLT3(Exception):
    pass


            
        
   # def add_triangle(self, number_of_triangles=1, disallow_lt1_triangle=True):
    
   #     vertices=[i for i in range(0,self.order()+number_of_triangles)]
        
    #    if disallow_lt1_triangle and len(vertices)-2<1:
    #        raise ValueError('Chosen number_of_triangles makes the zigzag have less than one triangle.')
        
    #    self.vertices=vertices
    #    return
    
  #  def remove_triangle(self):
  #      return Zigzag(self, triangles_count=self.triangles_count-1, parent_graph=None)
    
    #def degree(self, vertex):   # returns a dict, which     
    
# =============================================================================
# Function is_isomorphic(self, vr2, use_optimizations=True):
#       VectorRepresentation, VectorRepresentation -> bool
#
# Checks if self and vr2 represent isomorphic graphs.
# =============================================================================