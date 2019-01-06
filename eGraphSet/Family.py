#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 08:50:25 2018

@author: Mohamed Laradji
"""

# =============================================================================
# This library could be imported via:
#   from k5descendants.search import Family
# =============================================================================

#import family_set as fams
#import vector_representation as vrep

#from Exceptions import *

#from Pseudodescendant import Pseudodescendant

#from sage.graphs.graph_generators import graphs
#from sage.graphs.graph import Graph

#import thirdparty.boltons.setutils as setutils

#import collections
#import itertools
#import pickle
#import copy
#import time

from eGraph import DTEGraph, eGraph
from eGraphSet import eGraphSet
#from extended.eGraphIndexedSet import eGraphIndexedSet
#import ..common.graphs as cg
#import ..common.functions as cf

# =============================================================================
#
# =============================================================================

class Family(eGraphSet):
    '''
   Attributes:         
       self.expanded_triangle_types     dict -  This is a Graph to expanded triangle types dict (of form [a,b,c,d] where a,b,c,d in {0,1}).
       
       self.expanded    - dict          - This is an eGraph to Bool dictionary. The Bool values indicate whether the eGraph was fully expanded.
       self.version                     - This is a number indicating the version of the Family module.
       self.creation_date               - This is a string indicating when the family was created.
       self.modified_date               - This is a string indicating when the family was last modified.    
    '''

    type = 'Double Triangle Family'      # class variable shared by all instances  
    
    def __init__(self, *pargs, **kwargs):
        '''
        Initialize a Family by F=Family().
        '''
        
        super(Family, self).__init__(*pargs, **kwargs)
        
        self.tree=eGraph.eGraph(name="Family Tree", multiedges=False, loops=False, vertex_labels=True).to_directed() 
        
        self.expanded = dict()
        
        self._graph_class = DTEGraph.DTEGraph
        
        self.has_been_modified()

# =============================================================================
        
    @property
    def graph_class(self):
        '''
        The graph class of a Family object is the expected Python class of its graph members.
        '''
        
        return self._graph_class
    
# # =============================================================================      
    
#     def tree(self, conditions = dict()):
#         '''
#         Returns the family "tree", showing only the graphs that satisfy the conditions, if specified.
#         '''
        
#         graphs = self.restrict(conditions)
#         return self.tree.subgraph(graphs)
    
# =============================================================================

    def plot_tree(self, conditions = dict(), layout = 'acyclic', **kwargs):
        '''
        Plot the family tree, removing any vertices (from the plotted tree; the vertices remain in the full tree) which do not satisfy the specified conditions.
        '''
        
        graphs = set(self.member_iterator(conditions))
        return self.tree.subgraph(graphs).plot(layout = layout, **kwargs)
        
        
    
    def add_child(self, graph, parent = None, no_adding = False, convert_to_eGraph = True, **kwargs):
        '''
        This adds the graph to self and to self.tree if not a duplicate. Returns None if added, and if not, returns the duplicate of graph in self.
        
        Options:
            parent -    eGraph -    Default: None. If not None, adds an edge to self.tree between graph and parent.
            
            no_adding - bool -      If True, do not add the child to the family. Useful for when only the output of this function is desired.
        '''
        
        #child = graph.copy(immutable = True)
        
        if convert_to_eGraph:
            child = eGraph.eGraph_copy(graph, graph_class = self.graph_class, immutable = True)
        
        else:
            child = graph
        
        duplicate_graph = self.add_graph(child, no_adding = no_adding, **kwargs)
        
        if no_adding: return duplicate_graph
        
        if duplicate_graph is None: 
            #child = self[-1] # The child will be the most recent addition to self. This is a little hacky.
            self.tree.add_vertex(child) 
            self.set_expanded(child, False)
            child.family = self
        
        else: child = duplicate_graph
            
        if parent is not None: self.tree.add_edge(parent, child)
            
        self.has_been_modified()  
            
        return duplicate_graph
    

# =============================================================================
    

    def children_iterator(self, add_new_children = True, only_nonisomorphic = True, yield_preexisting_descendants = False, conditions = dict(), **kwargs):
        '''
        Returns an iterator over the children of descendants. The descendants expanded are the ones that fit the conditions. kwargs is passed to each graph.children_iterator and to self.set_expanded.
        
        Note that, unless yield_preexisting_descendants = True, only new children will be yielded.
        
        Options:
            add_new_children -  bool -      Whether or not to add the new children to the family. Functionality not tested when False. 
            
            only_nonisomorphic -    bool -      Whether to return only non-isomorphic children, or all labelled children.
            
            yield_preexisting_descendants -    bool -  Whether to output already existing descendants.
            
            conditions -    dict -  A count_name to count_value dictionary.
        '''
        
        # already_output_graphs contains references to all the graphs that have been output by this function.
        #   This is so children are not output more than once.
        
        already_output_graphs = set()
        
        for descendant in self.member_iterator(conditions): #, **kwargs):
            
            # Skip the descendant if it has already been expanded.
            if self.expanded[descendant]: continue
            
            # The children eGraphSet should speed up the isomorphism check process, especially if add_new_children = False.
            children = eGraphSet()
            
            # These lines is to yield preexisting children.
            if yield_preexisting_descendants and descendant not in already_output_graphs:
                yield descendant
                already_output_graphs.add(descendant)
            
 
            for child in descendant.children_iterator(**kwargs):
                
                # Check if child is in children of current descendant.
                duplicate_graph = children.add_graph(graph=child, require_nonisomorphic = only_nonisomorphic) 
                
                # Check if child is in self.
                if duplicate_graph is None:
                    duplicate_graph = self.add_child(child, parent=descendant, require_nonisomorphic = only_nonisomorphic, no_adding = not add_new_children)
                    
                
                if duplicate_graph is None:
                    # This means that child is a new graph.
                    
                    yield child
                    already_output_graphs.add(child.ecopy(immutable=True))                   
                
                else: child = duplicate_graph
    
            # All triangles in descendant have been expanded, so we set self.expanded[descendant] accordingly.    
            if add_new_children:
                self.set_expanded(descendant, **kwargs)
        
# =============================================================================

    def set_expanded(self, descendant, desired_expanded = True):
        '''
        Sets self.expanded[descendant] to the desired value.
        '''
        
        self.expanded[descendant] = desired_expanded
        
        self.has_been_modified()
    
# =============================================================================

                
    def descendants_iterator(self, conditions = dict(), only_nonisomorphic = True):
        '''
        This returns an iterable over the elements of self corresponding to the conditions. It will first iterate over elements already calculated, and then, if possible, calculates the next elements.
        
        Options:
            conditions -     dict -   Default: dict(). If empty dict, returns an iterator over all descendants.
        '''
        
        if 'order' in conditions:
            no_max_order = False
        else:
            no_max_order = True
            conditions['order'] = 3 # ***TODO*** Fix me.
        
            
        while no_max_order or conditions['order']>0:
        
            # First, we iterate over the preexisting members of self.

            for member in self.member_iterator(conditions = conditions):
                yield member


            # Next, we iterate over the children of preexisting members of self.
            
            if no_max_order:
                conditions['order'] += 1
            else:    
                conditions['order'] -= 1
                
            conditions['expanded'] = False
            
            for descendant in self.descendants_iterator(conditions):
                for child in descendant.children_iterator(only_nonisomorphic = only_nonisomorphic):
                    yield child

    
# =============================================================================
#     
#   Functions
#
# =============================================================================  

    
# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 