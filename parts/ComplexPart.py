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

from SimplePart import SimplePart

from ChordVector import ChordVector
from Zigzag import Zigzag, CannotMakeFirstVertex


## imports from common

#import common.graphs as g
#from common.exceptions import NotSubgraph, Underdefined
from common.exceptions import UnsupportedOption


# =============================================================================
# Class definitions 
# =============================================================================

class ComplexPart(SimplePart):
    '''
    This class aims to contain functions common to objects that are composed of SimpleParts such as zigzags and lone vertices.
    '''
    
    type = 'ComplexPart'
    
    ComplexPart_version=0.1
    
    
#-----------------  
# Object functions
#-----------------  

    

#-----------------  
# Vector functions
#-----------------  
    
    
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
    
    def is_proper(self): 
        '''
        # This function checks if all the parts follow the previous ones.
        '''
        
        if self.check_parts(): pass
        
        part_iterator=self.part_iterator()
        
        part1=part_iterator.next()
        
        try:
            part2=part_iterator.next()
            
            if not part2.follows(part1): return False
            
            part1=part2
            
        except StopIteration: 
            return True
        
    
    def append_part(self, part, side='both', sides=None, forced=False):
        '''
        This function attempts to append part to self.
        
        Options:
            side -      str -   'both' - Default option.   
                                    Try to append part to the left of self.parts, and if not possible, try to append to the right of self.parts.
                                'left' -    Try to append part to the left of self.parts.
                                'right' -   Try to append part to the right of self.parts.
            
            sides -     list -  List of side's to try. Expected to be a list of strings.
                                
            forced -    bool -  If False (default), checks if self allows part to be appended to it. If True, part will be added regardless.
            
        '''
        
        if forced:
            if side is 'right':
                self.parts.append(part)
                
            elif side is 'left':
                self.parts.insert(0,part)
                
            return
            
            
        else:
            if sides is None:
                if side is 'both':
                    sides=['left','right']
                
                elif side is 'left' or side is 'right':
                    sides=[side]
                 
                else:
                    raise UnsupportedOption('Only both, left, and right are supported. Received side = '+str(sides)+' instead.')
            
            try:
                side=sides.pop()
            
            except IndexError:
                raise CannotAppendPart('Part '+str(part)+' cannot be appended to ComplexPart '+str(self)+'.')
                
            try:
                self.make_follower(part, side=side.pop())
                return self.append_part(self, forced=True)
            
            except CannotMakeFollower:
                return self.append_part(self, side='right')
        
    def append_zigzag(self, zigzag, left_append=False):
        '''
        This function tries to attach zigzag to the right side of the chain.
            It also tries to attach it to the left side of the chain. If either 
            of these attachments are possible, it performs the attachment and 
            returns True. Otherwise, it returns False.
        
        If left_append=False, this function performs a right append, and if
            left_append=True, this function performs a left append. Note that
            you do not need to set left_append=True for a left_append, but
            if left_append=True, only left_appends will be tried.
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
                   
        if left_append: pass
            
        else:
            return self.append_zigzag(zigzag,left_append=True)
        
        
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
    

     
    
#-----------------     
# Graph
#-----------------  
        
    def graph(self, present_edges='full'):
        '''
        # This function creates a Graph object based on the contained parts (Zigzags, or LoneVertex's).
        #
        #
        #   Options:
        #       present_edges -   str -   Passed to ChordedComplexPart.
        '''
            
        graph=Graph()
        
        for part in self.part_iterator():
            graph=graph.union(part.graph(present_edges=present_edges))
    
        return graph
    
#-------------------      
# Counts
#------------------- 


    def triangles_count(self):
        '''
        # Returns the number of triangles.
        '''
        
        #if self.is_1zigzag: return g.triangles_count_Z(self.zigzags[0].triangles_count())
        
        triangles_count=0
        for part in iter(self.parts):
            triangles_count+=part.triangles_count()
            
        return triangles_count
 

# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 

class CannotAppendPart(Exception):
    '''
    Use when an operation requires a part to be appended to self, but it is not possible.
    '''
    
    pass