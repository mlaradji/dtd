#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 11:30:25 2018

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

from ..eGraph.PDGraph import PDGraph
from Family import Family
#from extended.eGraphIndexedSet import eGraphIndexedSet
from ..common import graphs as cg
from ..common import functions as cf

# =============================================================================
#
# =============================================================================

class K5Family(Family):
    '''
   Attributes:         
       self.expanded_triangle_types     dict -  This is a Graph to expanded triangle types dict (of form [a,b,c,d] where a,b,c,d in {0,1}).
       
       self.version                     - This is a number indicating the version of the Family module.
       self.creation_date               - This is a string indicating when the family was created.
       self.modified_date               - This is a string indicating when the family was last modified.    
    '''

    type = 'Family'      # class variable shared by all instances
    
    version = 0.1
    
    
    def __init__(self, add_K5=True):
        '''
        Initialize a Family by F=Family().
        '''
        
        super(K5Family, self).__init__()
        
        #self.tree=eGraph(name="Family Tree", multiedges=False, loops=False, vertex_labels=True).to_directed() 
        
        self.expanded_triangle_types=dict()
        
        if add_K5: self.add_K5()
        
        self.has_been_modified()

        
# =============================================================================      
        
       
    def add_K5(self):
        '''
        This adds the complete graph $K_5$ to the family.
        '''
        
        K5 = PDGraph(cg.K5())
        
        K5.allow_multiple_edges(False)
        K5.allow_loops(False)
        
        self.add_child(K5)
        
        return
    
    
# =============================================================================
    
    
#     def add_child(self, graph, parent=None, no_adding = False, **kwargs):
#         '''
#         This adds the graph to self and to self.tree if not a duplicate. Returns None if added, and if not, returns the duplicate of graph in self.
        
#         Options:
#             parent -    eGraph -    Default: None. If not None, adds an edge to self.tree between graph and parent.
            
#             no_adding - bool -      If True, do not add the child to the family. Useful for when only the output of this function is desired.
#         '''
        
#         duplicate_graph=self.add_graph(graph, no_adding = no_adding, **kwargs)
        
#         if no_adding: return duplicate_graph
        
#         if duplicate_graph is None: self.tree.add_vertex(child) 
        
#         else: child = duplicate_graph
            
#         if not parent is None: self.tree.add_edge(parent, child)
            
#         self.has_been_modified()  
            
#         return duplicate_graph
    

# =============================================================================
    
    
    def set_expanded_triangle_types(self, graph, expanded_triangle_types=[0,0,0,0], accept_zero_values=False):
        '''
        This sets self.expanded_triangle_types[graph] to expanded_triangle_types. Note that only non-zero changes will be considered. That is, if current self.expanded_triangle_types(graph)=[0,0,0,1], and expanded_triangle_types=[1,0,0,0], then the new self.expanded_triangle_types[graph] will be [1,0,0,1].
        
        Note that this function requires that graph is in self.
        
        Options:
            accept_zero_values -    bool -  Default: False. If True, zero changes will be considered. In the aforementioned example, the new self.expanded_triangle_types[graph] will be [1,0,0,0]
        '''
        
        check_expanded_triangle_types(expanded_triangle_types)
        
        self.check_membership(graph)  
        
        
        # The following copy is necessary in case expanded_triangle_types is linked to some other expanded_triangle_types.
        expanded_triangle_types=copy.copy(expanded_triangle_types)
            
        if accept_zero_values or graph not in self.expanded_triangle_types: 
            self.expanded_triangle_types[graph]=expanded_triangle_types
            return
            
        for i in range(0,len(expanded_triangle_types)):
            if expanded_triangle_types[i]: self.expanded_triangle_types[graph][i]=1
        
        self.has_been_modified()
        
        return
                
                
# =============================================================================


    def children_iterator(self, order = None, level = None, append_new_children = True, require_nonisomorphic = True, yield_preexisting_descendants = False, text=0, **kwargs):
        '''
        Returns an iterator over the children of descendants. The children will be of the desired_levels (expected to be None or an iterable object) if specified, and the descendants looked at are the ones that fit the conditions in kwargs, which are the same kwargs as for self.member_iterator().
        
        Note that only new children will be yielded.
        
        Options:
            order -         int -       Calculate only this order. Note that any DTE which would result in any other order will not be carried out. For calculation up to an order, see self.descendants_iterator.
            
            level -        set(int) -  Calculate these levels.
            
            append_new_children -   bool -      Whether or not to add the new children to the family. Functionality not tested when False. 
            
            require_nonisomorphic - bool -      Whether to return only non-isomorphic children, or all labelled children.
            
            yield_preexisting_descendants -     bool -  Whether to output already existing descendants.
            
            text -                  int -       How much text feedback to output. Note that this text only appears if the function is called from the module rather than the object (i.e. as Family.children_iterator(family, graph, **kwargs).
        '''
        
        # already_output_graphs contains references to all the graphs that have been output by this function.
        already_output_graphs = set()
        
        if text>0:
            print('---------------------------------------------------------')
        
        print(order)
        print(level)
        
        for descendant in self.member_iterator(order = order, level = level, **kwargs):
            
            # The children Family will be used to speed up the isomorphism check process, especially if append_new_children = False.
            
            children = Family()
            children.add_child(descendant)
            
            # This line is to yield preexisting descendants.
            
            if yield_preexisting_descendants and descendant not in already_output_graphs:
                
                yield descendant
                already_output_graphs.add(descendant)
            
            # Some text feedback
            
            if text>0:
                print('Descendant Index: '+str(self.index(descendant)))
                print('Pre-children Self ETT: '+str(self.expanded_triangle_types[descendant]))
            
            
            # Calculate desired_expanded_triangle_types, which indicates which triangle types we want to expand.
            
            current_expanded_triangle_types = self.expanded_triangle_types[descendant]
            
            triangle_types_tobe_expanded_kwargs = dict()
            triangle_types_tobe_expanded_kwargs['desired_order'] = order
            triangle_types_tobe_expanded_kwargs['desired_level'] = level
            triangle_types_tobe_expanded_kwargs['self_order'] = descendant.order()
            triangle_types_tobe_expanded_kwargs['self_level'] = descendant.level()
            triangle_types_tobe_expanded_kwargs['current_expanded_triangle_types'] = current_expanded_triangle_types
            
            desired_expanded_triangle_types = triangle_types_tobe_expanded(**triangle_types_tobe_expanded_kwargs)
            

            # Text feedback
            
            if text>0:
                print('Desired ETT: '+str(desired_expanded_triangle_types))
            
            
            if text>1:
                print('--------------')
                
                
            # Iterate over the children of descendant.
                
            children_iterator_kwargs = dict()
            #children_iterator_kwargs['current_expanded_triangle_types'] = current_expanded_triangle_types
            children_iterator_kwargs['desired_expanded_triangle_types'] = desired_expanded_triangle_types
            
            for child in descendant.children_iterator(**children_iterator_kwargs):
                
                duplicate_graph = children.add_child(graph=child, parent=descendant, require_nonisomorphic=require_nonisomorphic) # Check if child is in children of current descendant.
                
                if duplicate_graph is None:
                    duplicate_graph = self.add_child(graph=child, parent=descendant, require_nonisomorphic=require_nonisomorphic, no_adding = not append_new_children)
                    # Check if child is in self.
                
                if duplicate_graph is None:
                    # This means that child is a new graph.
                    
                    yield child
                    already_output_graphs.add(child)
                    
                    if text>1:
                        
                        if text<3:
                            print('Child Index: '+str(self.index(child)))
                            print('Child ETT: '+str(self.expanded_triangle_types[child]))
                        
                        print('Child added.')
                    

                
                else: child = duplicate_graph
                    
                if text>2:
                    
                    print('Child Index: '+str(self.index(child)))
                    print('Child ETT: '+str(self.expanded_triangle_types[child]))
                        
                if text>1:
                    print('--------------')
            
            if text>0:
                print('Post-children Self ETT: '+str(self.expanded_triangle_types[descendant]))
                    
            # If append_new_children, the children have been added to self. We will set self.expanded_triangle_types[descendant] to indicate the expanded triangle types.
             
            if text>2:
                for member in self:
                    print('Index: '+str(self.index(member))+'; ETT: '+str(self.expanded_triangle_types[member]))    
                
            if append_new_children:
                
                self.set_expanded_triangle_types(graph = descendant, expanded_triangle_types = desired_expanded_triangle_types, accept_zero_values = False) 
                
                if text>1:
                    print('expanded_triangle_types['+str(self.index(descendant))+'] set to '+str(desired_expanded_triangle_types)+'.')
            
            if text>2:
                for member in self:
                    print('Index: '+str(self.index(member))+'; ETT: '+str(self.expanded_triangle_types[member]))
            
            if text>0:
                print('---------------------------------------------------------')
                
        raise StopIteration
            
        
# =============================================================================

                
    def descendants_iterator(self, order = None, level = None, **kwargs):
        '''
        This returns an iterable over the elements of self corresponding to the options. It will first iterate over elements already calculated, and then, if possible, calculates the next elements.
        
        Options:
            order -     int -   Default: None. If None, returns all orders (Note that they are infinite in number!).
            level -     int -   Default: None. If None, all levels are returned.
        '''
        
        no_max_order = False
        
        if order is None:
            order = 0
            no_max_order = True
            
        while no_max_order or order>0:
        
            # First, we iterate over the preexisting members of self.

            for member in self.member_iterator(order = order, level = level, **kwargs):
                yield member


            # Next, we iterate over the children of preexisting members of self.

            for child in self.children_iterator(order = order, level = level, **kwargs):
                yield child

    
# =============================================================================
#     
#   Functions
#
# =============================================================================  
    

def check_expanded_triangle_types(expanded_triangle_types):
    '''
    This checks if expanded_triangle_types is of the right format. Passes without output if it is, and raises a TypeError if it isn't.
    '''
    
    if len(expanded_triangle_types)==4: pass
    else: raise TypeError('expanded_triangle_types must be a list of length 4. Received '+str(expanded_triangle_types)+' instead.')
        
    for triangle_type in iter(expanded_triangle_types):
        if triangle_type in {0,1}: pass
        else: raise TypeError('expanded_triangle_types can only contain 0s and 1s. Received '+str(expanded_triangle_types)+' instead.')
            
            
def triangle_types_tobe_expanded(desired_order=None, desired_level=None, self_order=None, self_level=None, current_expanded_triangle_types = [0,0,0,0]):
    '''
    Returns a list [a,b,c,d], where a,b,c,d in {0,1}, indicating which triangle types need to be expanded to get all children of self that have level in desired_orders and desired_levels. desired_orders and desired_levels are expected to be iterable objects.
    '''
    
    triangle_types_tobe_expanded = [0,0,0,0]
        
    if self_order is None or self_level is None:
        raise TypeError('Both self_order and self_level must be input.')
        
        
    desired_orders = cf.convert_to_iterable(desired_order, raise_None_exception = False)
    desired_levels = cf.convert_to_iterable(desired_level, raise_None_exception = False)
        
    if desired_orders is None:
        desired_orders = set([self_order+1])
    
    if not self_order+1 in desired_orders:
        # A DTE will increase the order by exactly 1. Thus, it is impossible to reach other orders.
        return [0,0,0,0]
    
    
    if desired_levels is None or self_level<0:  
        # This is to handle Z_3 (K_5) and Z_4 differently then the rest of descendants, which all have level>=0.
        return [1,1,1,1]



    for level in desired_levels:
        
        if level is None: continue
            
        if self_level==level:
            triangle_types_tobe_expanded[3]=1

        elif self_level==level-1:
            triangle_types_tobe_expanded[1]=1
            triangle_types_tobe_expanded[2]=1

        elif self_level==level-2:
            triangle_types_tobe_expanded[0]=1
            
            
    for i in range(0,len(current_expanded_triangle_types)):
        triangle_types_tobe_expanded[i]=triangle_types_tobe_expanded[i]-current_expanded_triangle_types[i]
                    
        if triangle_types_tobe_expanded[i]<0: triangle_types_tobe_expanded[i]=0
            
    triangle_types_tobe_expanded=[0,0,0,0]

    return triangle_types_tobe_expanded

# =============================================================================
#     
#   Naming
#
# ============================================================================= 
    
def K5Family_name(graph):
    
    # First, check if the graph is a zigzag.
    n = is_one_zigzag(G)
    if n != 0:
        return '$\hat{Z}_{}$'.format(n)
    else:
        pass
    
# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 