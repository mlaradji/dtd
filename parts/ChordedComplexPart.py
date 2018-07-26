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

from Part import Part

from ChordVector import ChordVector
from Zigzag import Zigzag, CannotMakeFirstVertex


## imports from common

#import common.graphs as g
#from common.exceptions import NotSubgraph, Underdefined
from common.exceptions import UnsupportedOption


# =============================================================================
# Class definitions 
# =============================================================================

class Complex(Part):
    '''
    This class aims to contain functions common to objects with defined chain and chord vectors.
    '''
    
    type = 'Complex'
    
    Complex_version=0.1
    
    
#-----------------  
# Object functions
#-----------------  
    
    
    def set_chord_vector(self, chord_vector=None, chord_edges=None, position_edges=None):
        '''
        # This function changes self.chord_vector to a ChordVector object using the defined arguments.
        #
        #   Options:
        #       *Note that only one of chord_vector, chord_edges, or position_edges should be defined, or an error is returned.*
        #       chord_vector -      list, tuple, or ChordVector -   Defines the ChordVector from a chord vector list or a ChordVector object.
        #       chord_edges -       list of 2-tuples -              Defines the ChordVector from the chord (non-triangle) edges.
        #       position_edges -    list of 2-tuples -              Defines the ChordVector from the position edges, which are the chord edges but with position (based on external vertices) labels instead of vertex labels.
        '''
    
        self.chord_vector=ChordVector(chord_vector, chord_edges=chord_edges, position_edges=position_edges, parent_object=self)
        
        self.is_1zigzag=False
        # Changing the chord_vector can change whether the chain is a onezigzag
        #   or not. Hence, self.is_1zigzag is set to False for consistency when 
        #   the chord vector is changed.
        
        return
    

#-----------------  
# Vector functions
#-----------------  
        
    def vector_pair(self):
        '''
        Returns a 2-tuple of the chain vector and chord vector of self (AKA vector pair).
        '''
        
        return tuple([self.chain_vector(),self.chord_vector.chord_vector()])
    
    
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
# Positions
#-----------------



#-------------
# Iterators
#-------------
        
        
    
#-----------------         
# Vertices
#----------------- 

    def vertices(self):
        '''
        # This function lists all the vertices in self.
        '''
        
        vertices=IndexedSet()
        
        for part in self.part_iterator():
            for vertex in part.vertex_iterator(ordered=True):
                vertices.add(vertex)
            
        return vertices
    
    
    def zigzag_vertices(self):
        '''
        # This function lists the list of vertices from each zigzag or lone vertex in self.
        '''
        
        zigzag_vertices=[]
        
        for part in self.part_iterator():
            zigzag_vertices.append(part.zigzag_vertices())    
            
        return zigzag_vertices
    
        
#-----------------         
# Edges
#-----------------          
    
    def chord_edges(self):
        '''
        List the chord edges of self. Chord edges are the edges encoded in the chord vector, which are the non-triangle edges of self.
        '''
        
        return self.chord_vector.chord_edges()
     
    
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
            chord_edges=self.chord_edges()
    
            graph.allow_multiple_edges(1)
            graph.add_edges(chord_edges)
    
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