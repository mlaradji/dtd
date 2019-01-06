#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 10:50:25 2018

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
from sage.graphs.graph import Graph

import boltons.setutils as setutils

import collections
import itertools
import copy
import time

from eGraph.eGraph import eGraph, eGraph_copy
#import common.graphs as cg
from common import functions as cf

# =============================================================================
#
# =============================================================================

class eGraphSet(setutils.IndexedSet):
    '''
   Attributes:   
       self.counts -                    dict -  This is an eGraph to dict dictionary, which currently contains 'order' and 'level'.
       
       self.expanded_triangle_types     dict -  This is a Graph to expanded triangle types dict (of form [a,b,c,d] where a,b,c,d in {0,1}).
       
       self.version                     - This is a number indicating the version of the Family module.
       self.creation_date               - This is a string indicating when the family was created.
       self.modified_date               - This is a string indicating when the family was last modified.    
    '''

    type = 'eGraphSet'      # class variable shared by all instances
    
    def __init__(self, *pargs, **kwargs):
        '''
        Initialize a Family by F=Family().
        '''
        
        super(eGraphSet, self).__init__(*pargs, **kwargs)
        
        self.creation_date=time.strftime('%Y-%m-%d_%H:%M:%S')
        self.modified_count=0
        
        #self.tree=Graph(name="Family Tree", multiedges=False, loops=False, vertex_labels=True).to_directed() 
        
        #self.expanded_triangle_types=dict() 
        
        self.has_been_modified()
        
        
# =============================================================================
    
        
    def has_been_modified(self):
        '''
        This is called whenever self is modified. It adds +1 to self.modified_count, and sets self.modified_date to current date.
        '''
        
        self.modified_count+=1
        self.modified_date=time.strftime('%Y-%m-%d_%H:%M:%S')
        return
    
    
# =============================================================================
    
    
    def count(self):
        '''
        Returns the number of graphs in self.
        '''
        
        return len(self)         
        
        
# =============================================================================    
    
    
    def add_graph(self, graph, require_nonisomorphic=True, no_adding=False):
        '''
        This adds an immutable copy of the graph to self. Returns None if added, and if not, returns the duplicate of graph in self.
        
        Options:
            require_nonisomorphic -     bool -      Whether to check for isomorphism.
            
            no_adding -                 bool -      Default: False. If True, graph is not added and self will not be modified, but the function still returns the same values.
        '''
        
        G = graph.copy(immutable = True)
        
        duplicate_graph=self.contains(G, isomorphic = require_nonisomorphic)
        
        if no_adding: return duplicate_graph
        
        if duplicate_graph is None:
            self.add(G)
        
        else:
            G = duplicate_graph
            
        self.has_been_modified()  
            
        return duplicate_graph

    
# =============================================================================
    
    
    def contains(self, graph, isomorphic=True, optimized=True):
        '''
        If graph is in self, or if an isomorphic copy of graph is in self (if isomorphic=True), returns that graph. Else, returns None.
        '''
        
        
        G = eGraph_copy(graph, immutable = True)
        
        
        try:
            self.check_membership(G)
            return G
        
        except IndexError:
            pass
        
        
        if not isomorphic: return None

        if optimized:
            restricted_set = self.member_iterator(conditions = {'order': G.order(), 'level': G.level()})
        
        else:
            # This is a safe fall back option if optimized doesn't work for any reason.
            restricted_set = self
            
        for H in restricted_set:
            if G.is_isomorphic(H): return H
            
        return
    
    
# ============================================================================= 


    def check_membership(self, graph):
        '''
        If graph is not in self, raises an IndexError. Otherwise, runs without any output.
        '''
        
        if graph in self: pass
        
        else:
            raise IndexError('graph is not in self.')
            
        return
                          

# =============================================================================

    def restrict(self, conditions = dict(), inplace = False):
        '''
        Returns a restricted version of self that only contains graphs satisfying the conditions.
        '''
        
        removed_graphs = set()
        
        for member in self.member_iterator(conditions, complement = True):
            removed_graphs.add(member)
            
        if inplace:
            self.difference_update(removed_graphs)
        
        if not inplace: 
            return self.difference(removed_graphs)
        

# =============================================================================
        
    def member_iterator(self, conditions = dict(), complement = False):
        '''
        Returns an iterator of the members of self that satisfy the imposed conditions. This functions takes the same kwargs as graph.satisfies_condiions.
        
        Options:
            complement - bool - If True, returns members that do not satisfy the conditions.
        '''
                    
        # Iterate over the descendants in self.
        
        for graph in self:
                
            if complement ^ graph.satisfies(conditions): yield graph
                

# =============================================================================


    def save(self, filename = None, extension = "egs", **kwargs):
        '''
        Function self.save(**kwargs): object -> None

        Saves self to disk. Returns without output if succesful. 

        Note that save requires both the pickle and dill modules to be installed.

        Options:
            filename -  str -   The filename to save self as. 
                                Default: "<self.type>_V<self.version>_M<self.modified_count>+"_D<self.modified_date>".
            extension - str -   The extension to append to filename. Default: "egs". If None, no extension is appended.
            path -      str -   The location to which the file should be saved. If unspecified, saves to "../data/".
            overwrite - bool -  Default: False. If True, overwrites the preexisting files. If False, raises a FileAlreadyExists exception if a file with the same name already exists.
        '''
        
        if filename is None:
            filename = self.type+"_V"+str(self.version)+"_M"+str(self.modified_count)+"_D"+str(self.modified_date)
        
        kwargs['extension'] = extension
        
        cf.save(self, filename, **kwargs)
            
        return
    
# # =============================================================================

#     def sort(self, conditions = list(), **kwargs):
#         '''
#         Function self.sort: eGraphSet -> eGraphSet
        
#         Options:
#             conditions - str to str OrderedDict - The conditions by which to sort.
#         '''
        
#         sorted_indices = sorted(range(len(self)), key = lambda i: self[i].count_list(conditions))
        
        
        
        
        
        
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