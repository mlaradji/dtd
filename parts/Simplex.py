#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 07:33:21 2018

@author: Mohamed Laradji
"""

# =============================================================================
# Import statements 
# =============================================================================

# imports 

from copy import copy

# imports from sage
#from sage.graphs.graph import Graph

# imports from thirdparty

try:
    from boltons.setutils import IndexedSet  # Note that this requires to be installed.

except ImportError:
    from ..thirdparty.boltons.setutils import IndexedSet
    
# imports from common
from ..common import graphs as g
from ..common.exceptions import NotSubgraph, Underdefined
#from common.exceptions import UnsupportedOption

# =============================================================================
# Class definitions 
# =============================================================================

class Simplex(object):
    '''
    A part is a graph that is a zigzag, a lone vertex, or a collection of parts.
    '''
    
    type = 'SimplePart'
    
    SimplePart_version = 0.1
    end_vertex_degree = 2
    parts = []
    
    
#-----------------  
# Object functions
#-----------------  

    @property
    def parent_object(self):
        '''
        Returns the parent object of self.
        '''
        
        return self._parent_object
    
    @parent_object.setter
    def parent_object(self, parent_object=None):
        '''
        Sets the parent object of self. Expects Pseudodescendant, Chain, or LoneVertex.
        '''
        
        self._parent_object=parent_object
        return
    
    
    def same_parent_object(self, part):
        '''
        Checks if self and part have the (exact) same parent_object.
        '''
        
        return self.parent_object is part.parent_object
    
    @property
    def max_degree(self):
        '''
        The maximum degree is perhaps more aptly called the saturation degree. Vertices of degree equal to this number are defined as saturated.
        '''
        return self._max_degree
    
    @max_degree.setter
    def max_degree(self, max_degree = 4):
        '''
        Sets the max_degree of self. This is used to distinguish between saturated (=max degree), under-saturated (<max_degree) and over-saturated (>max_degree) vertices.
        
        The default max_degree is 4.
        '''
        self._max_degree = max_degree
    
    @property
    def end_vertex_degree(self):
        '''
        End vertices of parts are vertices that can be identified without exceeding the max_degree. 
        
        The default end_vertex_degree is 2.
        '''
        
        return self._end_degree
    
    @end_vertex_degree.setter
    def end_vertex_degree(self, end_degree = 2):
        '''
        Sets the end vertex degree of self. 
        '''
        
        if type(end_degree) is int:
            self._end_vertex_degree = end_degree
            
        else:
            raise TypeError('end_vertex_degree must be an integer. Received '+str(end_vertex_degree)+' instead.')
    
    
#----------------- 
# Iterators
#-----------------
        
    
    def part_iterator(self):
        '''
        This function returns an iterable of the parts in self.
        '''        
        
        return iter(self.parts)
    
    
#----------------- 
# Positions
#-----------------
        
    def position_dict(self, position_to_vertex=True):
        '''
        # This function returns a position to vertex dict if position_to_vertex
        #   is True, and a vertex to position dict otherwise. The positions are
        #   are calculated based on the external vertices of the graph.
        '''
        
        position_index=0
        position_dict=dict()
        
        for vertex in iter(self.external_vertices()):
            
            if position_to_vertex: position_dict[position_index]=vertex
            else: position_dict[vertex]=position_index
            
            position_index+=1
            
        return position_dict
  

#-----------------         
# Vertices
#----------------- 
        
    
    def order(self):
        '''        
        Returns the number of vertices in self.
        '''
        
        return len(self.vertices)
        
    @property    
    def vertices(self):
        '''
        Returns a list of the vertices of self.
        '''
        
        return self._vertices
    
    @vertices.setter
    def vertices(self, value):
        '''
        Set self.vertices to this value.
        '''
        
        self._vertices = value
        
        
    def vertex_iterator(self, ordered=True):
        '''
        Returns an iterable of the vertices of self.
        '''
        
        return iter(self.vertices)
        
    
    def has_vertex(self,vertex):
        '''
        Returns True if vertex is a vertex of self, and False otherwise.
        '''
        
        for v in self.vertex_iterator():
            if v==vertex: return True
            
        return False
    
    @property    
    def external_vertices(self, present_edges='bare_skeleton'):
        '''
        # This function returns an IndexedSet of the external vertices of self.
        #   External vertices are vertices of degree<max_degree.
        #
        #   Options:
        #       present_edges -     str -   Same as for self.graph().
        '''
        
        external_vertices=IndexedSet()
        
        for vertex in self.vertex_iterator(ordered=True):
            remaining_degree=self.max_degree-self.degree(vertex, present_edges=present_edges)
            if remaining_degree>0: external_vertices.add(vertex)
            
        return external_vertices
    
    
    def end_vertices(self, present_edges='skeleton', side='both', nested=False, no_empty=True):
        '''
        # Returns the end vertices of self.
        #
        #   End vertices of parts are vertices that can be identified without exceeding the max_degree.
        #
        #   Options:
        #       present_edges -     str -   Same values as in self.graph(). 
        #
        #       side -              str -   Not implemented yet. 'both': Default value. Returns the list of end vertex sets of the parts.
        #                                   'left': Returns the end vertex set of the first part.
        #                                   'right': Returns the end vertex set of the last part.
        #
        #       nested -            bool -  True: Returns a nested list.
        #                                   False: Returns an IndexedSet.
        #
        #       no_empty -          bool -  True: Only non-empty sets are allowed.
        #                                   False: Empty sets are allowed.
        '''
        
        if nested:
            end_vertices=[]
            
        else:
            end_vertices=IndexedSet()
        
        graph=self.graph(present_edges=present_edges)
        
        
        for part in self.part_iterator():
            part_end_vertices=set()
            
            for vertex in part.vertex_iterator():
                if graph.degree(vertex)==self.end_vertex_degree:
                    part_end_vertices.add(vertex)
                    
            if no_empty and len(part_end_vertices)==0: continue
        
            else: 
                if nested:
                    end_vertices.append(part_end_vertices)
                    
                else:
                    end_vertices=end_vertices.union(part_end_vertices)
        
        
        return end_vertices
    
    
    def is_end_vertex(self, vertex=None, present_edges='skeleton' ):
        '''
        Checks if vertex is an end vertex of self.
        
        Options:
            present_edges -     str -   Same options as self.graph().
        '''
        
        if vertex is None:
            raise Underdefined('vertex needs to be defined.')
            
        end_vertices=self.end_vertices(present_edges=present_edges, side='both', nested=False)
        
        return vertex in end_vertices
    
    
    def end_vertices_intersection(self,part):
        '''
        This function lists the common end vertices in self and part and returns the common vertices and the 
            indices in which they occur. If there is no intersection, this function will return False.
        
        If the ith zigzag and jth zigzag in self and chain, respectively, have the common end vertex v then [i,j,v] will be appended to the returned list.
        
        
        Example:    C1=Chain([2,2])
                    print(C1.zigzag_vertices())
                    >>> [[0,1,2,3], [3,4,5,6]]
                    Z=Zigzag(vertices=[7,6,8])
                    print(Z.zigzag_vertices())
                    >>> [[7, 6, 8]]
                    C1.end_vertices_intersection(Z)
                    >>> [[1, 0, 6]]
        '''
        
        intersections=[]
        
        part1_end_vertices_list=self.end_vertices(nested=True)
        part2_end_vertices_list=part.end_vertices(nested=True) 
        
        for i in range(0, len(part1_end_vertices_list)):
            for j in range(0,len(part2_end_vertices_list)):
                intersection=part1_end_vertices_list[i].intersection(part2_end_vertices_list[j])
                for vertex in intersection:
                    
                    intersections.append([i,j,vertex])
                    
                    #if vertex==self.first_vertex():
                    #elif vertex==self.last_vertex():
                        #intersections.append([i,j,vertex,-1])
         
        if len(intersections)>0:
            return intersections
        else:
            raise NoIntersection('self and part do not have any end vertices in common.')

      
#-----------------         
# Edges
#-----------------              
    
    def edges(self): 
        '''
        List all the edges of self, including triangle edges and non-triangle (or chord) edges.
        '''
        
        return self.graph().edges()  
    
    
#-----------------    
# First and last
#-----------------
        
    def first_vertex(self): 
        '''
        Returns the first vertex of self.
        '''
        
        return self.vertex_list()[0]
    
    
    def last_vertex(self): 
        '''
        Returns the last vertex of self.
        '''
        
        return self.vertex_list()[-1]
    
    
    def first_part(self):
        '''
        Returns the first part of self.
        '''
        
        return self.parts[0]
    
    
    def last_part(self):
        '''
        Returns the last part of self.
        '''
    
        return self.parts[-1]
    
    
    def follows(self, part):
        '''
        # follows returns 1 if the first vertex of self and the last vertex of part are the same, -1 if the last vertex of self and the last vertex of part are the same, and 0 otherwise.
        #
        # Options:
            part: Part object.
        '''
        
        if self.first_vertex()==part.last_vertex(): return 1
        elif self.last_vertex()==part.last_vertex(): return -1
        else: return 0
        
        
    def is_followed_by(self, part):
        '''
        # is_followed_by returns 1 if the last vertex of self and the first vertex of part are the same, -1 if the first vertex of self and the first vertex of part are the same, and 0 otherwise.
        #
        # Options:
            part: Part object.
        '''
        
        if self.last_vertex()==part.first_vertex(): return 1
        elif self.first_vertex()==part.first_vertex(): return -1
        else: return 0
     
    
#-----------------     
# Graph
#-----------------  
           
    def degree(self, vertex=None, present_edges='full'):
        '''
        # If vertex is defined, returns degree(vertex). Else, returns a list of all vertex degrees.
        #
        #   Options:
        #       vertex -            int -   Indicate a specific vertex in the graph.
        #       present_edges -     str -   Same possible values as in self.graph().
        '''
        
        return self.graph(present_edges=present_edges).degree(vertex)
    
    
    def plot(self, present_edges='full'): 
        '''
        # Plots the graph of self.
        '''
        
        return self.graph(present_edges=present_edges).plot()
  
    
#-----------------  
# Bare skeleton
#-----------------  
        
    def bare_skeleton(self): 
        '''
        The bare skeleton is a graph containing only triangle edges. This returns the Graph object of the bare skeleton of self.
        '''
        
        return self.graph(present_edges='bare_skeleton')
    
    
    def bare_skeleton_degree(self, vertex=None):
        '''
        # If vertex is defined, returns degree(vertex) in the bare skeleton of self. Else, returns a list of all vertex degrees.
        '''
        
        return self.degree(vertex,present_edges='bare_skeleton')
    
    def bare_skeleton_plot(self):
        '''
        # Plots the bare skeleton of self.
        '''
        
        return self.plot(present_edges='bare_skeleton')
    
    
#-----------------      
# Skeleton
#-----------------  
        
    def skeleton(self):
        '''
        The skeleton is a graph containing only triangle edges and internal chord edges of the parts.
        '''
        
        return self.graph(present_edges='skeleton')
    
    
    def skeleton_degree(self, vertex=None):
        '''
        # If vertex is defined, returns degree(vertex) in the skeleton of self. Else, returns a list of all vertex degrees.
        '''
        
        return self.degree(vertex,present_edges='skeleton')
    
    
    def skeleton_plot(self):
        '''
        # Plots the skeleton of self.
        '''
        
        return self.plot(present_edges='skeleton')
    
#-----------------    
# Graph operations
#-----------------
        
    def is_subgraph(self, graph, induced=True, isomorphism=False):
        '''
        # Function is_subgraph: Pseudodescendant (self), Pseudodescendant or Graph -> bool
        #
        #   Returns True if self is a subgraph of graph, and False otherwise.
        #
        #   Options:
        #       induced         - bool  - If True, checks if self is an induced subgraph of graph.
        #       isomorphism     - bool  - If True, function returns whether self is isomorphic to some subgraph of graph.
                                            If False, function returns whether self is a labelled subgraph of graph.
        '''
        
        # Note: it might be worthwhile defining a new type for our objects.
        
        #   H - self
        #   G - other graph
        
        H=self.graph()
        G=g.get_graph(graph)
                
        if isomorphism:
            return G.subgraph_search(H, induced=induced)
        
        else:
            # .is_subgraph currently has problems with multiple edges. Multiple
            #   edges will be disabled before the check (on copies of the graphs).
            
            G2, H2 = copy(G), copy(H)
            
            G2.allow_multiple_edges(0)
            H2.allow_multiple_edges(0)
            
            return H2.is_subgraph(G2, induced=induced)
        
    
    def graph_difference(self, graph, reverse_positions=False, induced=False):
        '''
        # graph_difference: Pseudodescendant, Graph -> list of 2-tuples (the edges)
        #      
        #   This function first checks if self is a subgraph of graph. Next, it
        #       creates a list of the edges in graph but not in self.
        #
        #   Options:
        #       reverse_positions -     bool -  If True, returns E(graph)\E(self). If not, returns E(self)\E(graph).
        #       induced -               bool -  If True, returns only the edges incident to vertices common to both graphs.
                                                If False, returns all the edges.
        '''
        
        if reverse_positions: G, H = copy(graph), copy(self)
        else: G, H = copy(self), copy(graph)
        
        if not H.is_subgraph(G, induced=False):
            raise NotSubgraph('H ('+str(H)+') must be a subgraph of G ('+str(G)+').')
            
        G, H = g.get_graph(G), g.get_graph(H)
        
        if induced: G=G.subgraph(H.vertices())
            
        return set(G.edges()).difference(H.edges())
    
    
    def is_isomorphic(self, graph, optimizations=False):
        '''
        #   Function is_isomorphic: Pseudodescendant, Pseudodescendant or Graph -> bool
        #
        #   Returns True if isomorphic, and False otherwise.
        #
        #   Options:
        #       optimizations - bool - Not implemented yet. Has no effect.
        #
        #   There are some optimizations that could be coded here, such as checking
        #   chain vectors.
        '''
        
        G=self.graph()
        H=g.get_graph(graph)
        
        return G.is_isomorphic(H) 
    

#-------
#Checks
#-------

    def check_parts(self):
        '''
        Check if self.parts is of the right type and is non-empty. Returns True if it is, and raises an exception otherwise.
        '''
        
        try:
            len(self.parts) #Anything with length should work as self.parts.
        except TypeError:
            raise TypeError('self.parts must be a type with length (such as list, deque, and IndexedSet). Received '+str(self.parts)+' instead.')
            
        if len(self.parts)==0: 
            raise EmptyPartsList('Expected non-empty self.parts. Received '+str(self.parts)+' instead.')
            
        # It is probably useful to add a check of the members of self.parts.
        
        return True
    
    
# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 

    
class EmptyPartsList(Exception):
    '''
    Use when an operation requires a non-empty self.parts but self.parts is either empty or of the wrong type.
    '''

    pass


class NoIntersection(Exception):
    '''
    Use when two sets do not intersect, but they need to be.
    '''

    pass