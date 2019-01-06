#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 07:53:02 2018

@author: Mohamed Laradji
"""

# =============================================================================
# Import statements 
# =============================================================================


## imports from sage

#from sage.graphs.graph import Graph

## imports from thirdparty

from copy import copy

# try:
#     from boltons.setutils import IndexedSet  # Note that this requires to be installed.

# except ImportError:
#     from ..thirdparty.boltons.setutils import IndexedSet
    
## imports from pseudodescendants

from Complex import Complex, CannotAppendPart
from Zigzag import Zigzag, CannotMakeFirstVertex


## imports from common

from ..common import graphs as g
from ..common.exceptions import NotSubgraph, Underdefined
#from common.exceptions import UnsupportedOption


# =============================================================================
# Class definitions 
# =============================================================================


class Chain(Complex):
    '''
    Chain object contains the functions common to both open and closed chains.
    A chain is composed of zigzags, and it inherits from the class ComplexPart.
    '''
    
    type = 'Chain'      # class variable shared by all instances
    
    Chain_version=0.1

    def __init__(self, chain_vector=None, zigzag=None, start_at=0, parent_object=None):
        '''
        A Chain object can be initialized in several ways. The chain_vector can be set to a list of integers, with positive values denoting the triangles count in a zigzag, 0 denoting a gap, and negative values denoting non-triangle vertices. If called with no arguments (i.e. Chain()), then chain_vector defaults to [1], which will create a chain with one 1-triangle zigzag. If called with zigzag set to some Zigzag object, it will create a Chain containing that Zigzag. 
        
        Options:
            start_at -      int -   The vertex labelling starts at this value. If the Chain object
                                        is initialized by zigzag, starting_vertex will be ignored.
            parent_object - Part -  The parent_object will be set to this.
        '''
        
        #self.is_1zigzag=False
        #self.same_first_and_last_vertex=False
        
        if zigzag is None:
            if chain_vector is None: chain_vector=[1]
            self.make_zigzags(chain_vector)
            
            #if closed: self.make_closed()
        
            self.reindex(start_at = start_at) 
            
            
        if zigzag is not None:
            # This means that a Zigzag object is the argument. Note that this
            #   will ignore the chain_vector and closed arguments. It it is po-
            #   -tentially useful to write some extra lines to deal with the c-
            #   -ses when both chain_vector and zigzag are defined.
            zigzag.set_parent_object(self)
            self.parts=[zigzag]
        
        #if not chord_vector: chord_vector=tuple([])
        #self.set_chord_vector(chord_vector)
        
        self.parent_object = parent_object
    
    
    def chain_vector(self):
        chain_vector=[]
        for zigzag in iter(self.zigzags):
            chain_vector.append(zigzag.triangles_count())
            
        if self.is_1zigzag or self.same_first_and_last_vertex: pass
        else: chain_vector.append(0)
        
        return tuple(chain_vector)
        
    
    def make_zigzags(self, chain_vector=None):
        if not chain_vector: chain_vector=self.chain_vector()
        
        parts=[]
        
        for triangles_count in iter(chain_vector):
            if triangles_count>0:
                parts.append(Zigzag(triangles_count, parent_object=self))
            else:
                raise ValueError('The chain vector should only contain positive integers.')
               
        self.parts=parts
        
        self.reindex()
        
        return
    
    
    def identify_first_and_last_vertex(self):
        self.zigzags[-1].vertices[-1]=self.zigzags[0].vertices[0]
        return self.zigzags[-1].vertices[-1]
    
    @property
    def same_first_and_last_vertex(self):
        return self.zigzags[-1].vertices[-1] is self.zigzags[0].vertices[0]
    
    def make_closed(self):
        '''
        # This function makes the chain closed. ie, if there is only one zigzag,
        #   it will add edges to make the graph 4-regular by changing the chord
        #   vector. If there is more than one zigzag, it will identify the first
        #   and last vertices.
        '''
        
        if len(self.zigzags)==1:
            triangles_count=self.zigzags[0].triangles_count()
            if triangles_count==1:
                self.set_chord_vector((1,-1,1))
            elif triangles_count>1:
                self.set_chord_vector((2,-1,2))
                
            self.is_1zigzag=True
                    
        elif len(self.zigzags)>1:
            self.identify_first_and_last_vertex()

        return               

    


    
#    def is_closed(self):    # Needs work.
#        if self.is_proper():
#            if len(self.zigzags)==1:
#                if self.zigzags[0].triangles_count()==1:
#                    if self.chord_vector==(1,-1,1): return True
#                    else: return False
#                elif self.chord_vector==(2,-1,2): return True
#                else: return False    
#            elif self.zigzags[0].follows(self.zigzags[-1]): return True
#            else: return False
                  
#        else: return False
        
#    def is_open(self):
#        if self.is_proper() and not self.zigzags[0].follows(self.zigzags[-1]):
#            return True
#        else: return False
        
#    def follows(self, chain):
#        if self.is_open() and chain.is_open() and self.zigzags[0].follows(chain.zigzags[-1]):
#            return True
#        else: return False
    
#    def is_followed_by(self, chain):
#        if self.is_open() and chain.is_open() and chain.zigzags[0].follows(self.zigzags[-1]):
#            return True
#        else: return False
        
        
    def zigzag_iterator(self): return iter(self.zigzags)
    
#    def part_iterator(self): return self.zigzag_iterator()
    
    def last_zigzag(self): 
        '''
        Returns the last zigzag of self.
        '''
        
        return self.last_part()
    
    def first_zigzag(self): 
        '''
        Returns the first zigzag of self.
        '''
        
        return self.first_part()
    
    @property
    def zigzags(self):
        '''
        Returns the zigzags of self.
        '''
        
        return self.parts
        
    
    def append_zigzag(self, zigzag, left_append=False):
        '''
        # This function tries to attach zigzag to the right side of the chain.
        #   It also tries to attach it to the left side of the chain. If either 
        #   of these attachments are possible, it performs the attachment and 
        #   returns True. Otherwise, it returns False.
        #
        # If left_append=False, this function performs a right append, and if
        #   left_append=True, this function performs a left append. Note that
        #   you do not need to set left_append=True for a left_append, but
        #   if left_append=True, only left_appends will be tried.
        '''
        
        end_vertices_intersection=self.end_vertices_intersection(zigzag)
        
        if end_vertices_intersection:
            for intersection in iter(end_vertices_intersection):
                
                vertex=intersection[2] # 0- ith index, 1- jth index, 2- vertex
                
                # Only consider intersections with the last zigzag of self.
                #   Or with first_zigzag if left_append=True.

                if left_append and self.first_zigzag() is self.zigzags()[intersection[0]]:
                    try:
                        zigzag.make_first_vertex(vertex, make_last_vertex=True)
                        self.first_zigzag().make_first_vertex(vertex)
                        zigzag.parent_chain=self
                        self.zigzags.insert(0,zigzag)
                            
                    except CannotMakeFirstVertex: continue
                    
                elif self.last_zigzag() is self.zigzags()[intersection[0]]:
                    try:    
                        zigzag.make_first_vertex(vertex)
                        self.last_zigzag().make_first_vertex(vertex, make_last_vertex=True)
                        zigzag.parent_chain=self
                        self.zigzags.append(zigzag)
                        
                    except CannotMakeFirstVertex: continue        
                
                return True
                   
        if left_append:
            raise CannotAppendPart('Zigzag '+str(zigzag)+' cannot be appended '
                                     'to chain '+str(self)+'.')
        else:
            return self.append_zigzag(zigzag,left_append=True)