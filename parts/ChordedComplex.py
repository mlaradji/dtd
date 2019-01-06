#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 07:33:21 2018

@author: Mohamed Laradji
"""

# =============================================================================
# Import statements 
# =============================================================================


## imports from sage

from sage.graphs.graph import Graph

## imports from thirdparty

#from copy import copy

try:
    from boltons.setutils import IndexedSet  # Note that this requires to be installed.

except ImportError:
    from thirdparty.boltons.setutils import IndexedSet
    
## imports from pseudodescendants

from Complex import Complex

from ChordVector import ChordVector
from Zigzag import Zigzag, CannotMakeFirstVertex


## imports from common

#import common.graphs as g
#from common.exceptions import NotSubgraph, Underdefined
from ..common.exceptions import UnsupportedOption


# =============================================================================
# Class definitions 
# =============================================================================

class ChordedComplex(Complex):
    '''
    This class aims to contain functions common to objects with defined chain and chord vectors.
    '''
    
    type = 'ChordedComplex'
    
    #Complex_version=0.1
    ignore_oversaturated = False
    
#-----------------  
# Object functions
#-----------------  
    @property
    def chord_vector(self):
        return self._chord_vector
    
    @chord_vector.setter
    def chord_vector(self, chord_vector=None,):
                     #chord_edges=None, position_edges=None):
        '''
        # This function changes self.chord_vector to a ChordVector object using the defined arguments.
        #
        #   Options:
        #       *Note that only one of chord_vector, chord_edges, or position_edges should be defined, or an error is returned.*
        #       chord_vector -      list, tuple, or ChordVector -   Defines the ChordVector from a chord vector list or a ChordVector object.
        #       chord_edges -       list of 2-tuples -              Defines the ChordVector from the chord (non-triangle) edges.
        #       position_edges -    list of 2-tuples -              Defines the ChordVector from the position edges, which are the chord edges but with position (based on external vertices) labels instead of vertex labels.
        '''
    
        self._chord_vector=ChordVector(
            chord_vector,
            parent_object=self,
        ) #chord_edges=chord_edges, position_edges=position_edges, parent_object=self)
        
#         self.is_1zigzag=False
#         # Changing the chord_vector can change whether the chain is a onezigzag
#         #   or not. Hence, self.is_1zigzag is set to False for consistency when 
#         #   the chord vector is changed.
    

#-----------------  
# Vector functions
#-----------------  
    
    @property
    def vector_pair(self):
        '''
        Returns a 2-tuple of the chain vector and chord vector of self (AKA vector pair).
        '''
        
        return tuple([self.chain_vector, self.chord_vector.vector])
    
    
#------------------     
# Part manipulation
#------------------  
        
    def reindex(self, start_at=0):
        '''
        # This function reindexes all the vertices in the zigzags so that they
        #   are sequential. Note that this changes the chain. This function
        #   returns the last vertex_index.
        #
        #   Options:
        #       start_at -  integer -   The integer at which the labelling for the vertices should start. Default is 0.
        '''
        
        vertex_index=start_at
        
        for part in self.part_iterator():
            vertex_index=part.reindex(start_at=vertex_index)
            
        if self.same_first_and_last_vertex:
            self.identify_first_and_last_vertex()
            vertex_index-=1
        
        return vertex_index
    
    
#----------------- 
# ChordVector
#-----------------

    @property
    def edges(self,):
              #chord_vector=None, parent_object=None):
        
        # This function creates a list of edges based on the positions (rather
        #   than vertex labels). That is, (i,j) means position i is adjacent to 
        #   position j. Note that the if parent_object is not None, it will be 
        #   used instead of self.parent_object.
        #
        #   If make_positions=True, the output will be a list of two items,
        #       the position_edges and positions lists.
        
#         if parent_object is None: 
#             if self.parent_object is None:
#                 raise ce.MissingParentObject('make_position_edges requires a parent object. Either set the parent object using self.set_parent_object, or use the argument parent_object.')
                
#             else:    
#                 parent_object=self.parent_object
        
#         if chord_vector is None: return []
        
        #skeleton_degree=self.parent_object.skeleton_degree()
        
        # external_vertices() is expected to return an ordered list of vertices.
        external_vertices = list(self.external_vertices)
        
        remaining_degree = {
            vertex: self.max_degree - self.bare_skeleton_degree(vertex) for vertex in self.external_vertices
        }
        
        position_edges, chord_edges = [], []
        
        chords = iter(self.chord_vector.vector) 
        
        for chord in chords:
            try:
                index1 = 0
                # Find the first vertex that is unsaturated.
                while remaining_degree[external_vertices[index1]]<=0:
                    del external_vertices[index1]
                    
                vertex1 = external_vertices[index1]
            
                # Add the chord length to find the first unsaturated vertex2.
                index2 = chord%len(external_vertices)
                while remaining_degree[external_vertices[index2]]<=0:
                    del external_vertices[index2]
                    index2 = chord%len(external_vertices)
                
                vertex2 = external_vertices[index2]
                
                ## Find the first j such that vertex[j] is unsaturated.
                #while remaining_degree[j]<=0:
                    #j += 1
            
            except IndexError:
                if self.ignore_oversaturated: break
                else:
                    raise OverSaturated('Every vertex in the graph has degree >= self.max_degree = {}. Either increase self.max_degree, or set ChordVector.ignore_oversaturated to True. In the future, we would like to implement an option for infinite max_degree.'.format(self.max_degree))
            
            #vertex1 = self.external_vertices[i]
            #vertex2 = self.external_vertices[j]
         
            #position_edges.append((i, j))
            chord_edges.append((vertex1, vertex2))
            
            remaining_degree[vertex1]-=1
            remaining_degree[vertex2]-=1
        
        return {
            'position': position_edges, 
            'chord': chord_edges,
        }
    
    @property
    def chord_edges(self):
        # This function creates a list of chord edges based on the external vertices
        #   and the supplied chord_vector or self.chord_vector
        
        
#         if parent_object is None: 
#             if self.parent_object is None:
#                 raise ce.MissingParentObject('chord_edges requires a parent object. Either set the parent object using self.set_parent_object, or define the argument parent_object.')
                
#             else:    
#                 parent_object=self.parent_object
        
        #if self.chord_vector is None: return []
        
#         position_edges = self.position_edges
        
#         position_dict = self.parent_object.position_dict(position_to_vertex=True)
        
#         chord_edges=[]
        
#         for position_edge in iter(position_edges):
#             chord_edge=(position_dict[position_edge[0]], position_dict[position_edge[1]])
#             chord_edges.append(chord_edge)
            
        return self.edges['chord']
    
    @property
    def position_edges(self):
        #return self.make_position_edges(self.chord_vector)
        return self.edges['position']
    
    def positions(self, parent_object=None, with_labels=False):
        if parent_object is None: 
            if self.parent_object is None:
                raise ce.MissingParentObject('positions requires a parent object. Either set the parent object using self.set_parent_object, or use the argument parent_object.')
                
            else:    
                parent_object=self.parent_object
                
        external_vertices=self.parent_object.external_vertices()
        
        if with_labels: return external_vertices
        else: return [i for i in range(0,len(external_vertices))]
        
    def no_of_positions(self):
        # This function counts the number of positions, based on the parent object.
        return len(self.positions())
        
    
#     def set_max_degree(self, max_degree=4):
        
#         self.max_degree=max_degree
#         return self.max_degree
    
#     def set_parent_object(self, parent_object=None):
        
#         self.parent_object=parent_object
#         return self.parent_object
    
#     #def set_chord_vector(self, chord_vector=None):
        
#   #      if chord_vector is None or type(chord_vector) is tuple or type(chord_vector) is list:
#  #           self.chord_vector=chord_vector
#   #          return
            
#   #      elif chord_vector.type is 'ChordVector':
#  #           self.chord_vector=chord_vector.chord_vector
#  #           self.set_parent_object(chord_vector.parent_object)
#  #          return
        
#  #       else:
#  #           raise TypeError('chord_vector must be None or of type tuple, list, or ChordVector.')
    
    def position_dict(self, position_to_vertex=True):
        # This function calls self.parent_object.position_dict(), which returns
        #   a position to vertex dict if position_to_vertex=True, and a vertex
        #   to position dict otherwise.
        
        if self.parent_object is None: 
            raise ce.MissingParentObject('ChordVector.position_dict requires calling self.parent_object.position_dict, but parent_object is None.')
        
        return self.parent_object.position_dict(position_to_vertex)

#-------------
# Iterators
#-------------
        
        
    
#-----------------         
# Vertices
#----------------- 

#     def vertices(self):
#         '''
#         # This function lists all the vertices in self.
#         '''
        
#         vertices=IndexedSet()
        
#         for part in self.part_iterator():
#             for vertex in part.vertex_iterator(ordered=True):
#                 vertices.add(vertex)
            
#         return vertices
    
    
#     def zigzag_vertices(self):
#         '''
#         # This function lists the list of vertices from each zigzag or lone vertex in self.
#         '''
        
#         zigzag_vertices=[]
        
#         for part in self.part_iterator():
#             zigzag_vertices.append(part.zigzag_vertices())    
            
#         return zigzag_vertices
    
        
#-----------------         
# Edges
#-----------------          
    
#     @property
#     def chord_edges(self):
#         '''
#         List the chord edges of self. Chord edges are the edges encoded in the chord vector, which are the non-triangle edges of self.
#         '''
        
#         return self.chord_vector.chord_edges()
     
    
#-----------------     
# Graph
#-----------------  
        
    def graph(self, present_edges='full'):
        '''
        # This function creates a Graph object based on the contained parts (Zigzags, Chains or LoneVertex's).
        #
        #   We define three different graphs: bare_skeleton, skeleton, and graph. 
        #       The main difference between the three is the presence of chord edges.
        #       In bare_skeleton, the skeleton function is used for all the parts, and 
        #       so there should be no chord edges. In skeleton, chains with defined 
        #       (internal) chord vectors would result in those chord edges showing up 
        #       in the graph. In graph, both the internal chord vectors of chains, when
        #       it is defined, and the chord vector of the pseudodescendant, show up,
        #       and this should result in a 4-regular graph if all is well.
        #
        #   Options:
        #       present_edges -   str -   'full', 'bare_skeleton', or 'skeleton'. Default is 'full'.
        '''
       
        if type(present_edges) is str:        
            if present_edges is 'bare_skeleton':
                internal_chord_edges=False
                external_chord_edges=False 
                triangle_edges=True                        
            
            elif present_edges is 'skeleton': 
                internal_chord_edges=True 
                external_chord_edges=False 
                triangle_edges=True
            
            elif present_edges is 'full':
                internal_chord_edges=True 
                external_chord_edges=True
                triangle_edges=True
                
            elif present_edges is 'only_chords':
                internal_chord_edges=True 
                external_chord_edges=True
                triangle_edges=False
                
            elif present_edges is 'only_internal_chords':
                internal_chord_edges=True 
                external_chord_edges=False
                triangle_edges=False
                
            elif present_edges is 'only_external_chords':
                internal_chord_edges=False 
                external_chord_edges=True
                triangle_edges=False
                
            elif present_edges is 'only_vertices':
                internal_chord_edges=False
                external_chord_edges=False
                triangle_edges=False
        
            else:
                raise UnsupportedOption('present_edges= '+present_edges+' is not a valid option. Supported options are bare_skeleton, skeleton, and full.')
                
        else:
            raise TypeError('present_edges must be of type str (string). Got '+str(type(present_edges))+' instead.')
            
        graph=Graph()
        
        for part in self.part_iterator():
            if internal_chord_edges:
                graph=graph.union(part.graph(present_edges='full'))
            else:
                graph=graph.union(part.graph(present_edges='skeleton'))
            
        if external_chord_edges:
            graph.allow_multiple_edges(1)
            graph.add_edges(self.chord_edges)
    
        return graph
    
#-------------------      
# Isomorphism Checks
#------------------- 
        
    def is_n_zigzag(self):
        '''
        # If self is an n-zigzag, returns n. Otherwise, returns 0.
        '''
        
        chain_vector, chord_vector=self.vector_pair()
        
        chain_vector_length,no_of_chords=len(chain_vector),len(chord_vector)
        
        if chain_vector_length==1 and no_of_chords==0:
            return 1
        elif chain_vector_length>1 and chain_vector_length==no_of_chords:
            return chain_vector_length
        else:
            return 0   
        
#-------------------      
# Exceptions
#------------------- 

class OverSaturated(Exception):
    '''
    This exception is to be raised when all vertices in an object exceed the max_degree.
    '''
    
    pass
