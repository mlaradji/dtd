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

import thirdparty.boltons.setutils as setutils

import collections
import itertools
import pickle
import copy
import time

from eGraph.eGraph import eGraph, eGraph_copy
#from extended.eGraphIndexedSet import eGraphIndexedSet
import common.graphs as g
import common.functions as f

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
    
    version=0.1
    
    
    def __init__(self):
        '''
        Initialize a Family by F=Family().
        '''
        
        super(eGraphSet, self).__init__()
        
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

        
    def member_iterator(self, **kwargs):
        '''
        Returns an iterator of the members of self that satisfy the imposed conditions. This functions takes the same kwargs as graph_satisfies_condiions. Currently, only order and level have been implemented.
        '''
                    
        # Iterate over the descendants in self.
        
        for graph in self:
                
            if graph.satisfies_conditions(**kwargs): yield graph
                

# =============================================================================


    def save(self,filename=None, path=None):
        '''
        Function self.save(savename, path): str, str -> None
        
        Saves the family to disk.
        
        Options:
            filename -  str -   If filename is specified, this saves self to filename+".family". If filename is not specified, this saves self to "family_"+str(self.family_version)+"_"+str(self.modified_count)+"_"+str(self.modified_date)+".family".
            path -      str -   If unspecified, saves to "../data".
        '''
        
        if filename is None:
            filename="family_"+str(self.family_version)+"_"+str(self.modified_count)+"_"+str(self.modified_date)
            
        if path is None:
            path="../data/"
        
        with open(path+filename+".family", "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
            
        return
    

    
# =============================================================================
#     
#   Functions
#
# ============================================================================= 


def load(filename, path=None):
    '''
    Function load(savename, path): str, str -> object
        
    Loads a file from disk.
    
    Usage:
        family=None
        family=load(family_2.family, path="../data/")
        
    Options:
        filename -  str -   The full filename to load. Note that, unlike Family.save, ".family" is not appended to the filename.
        path -      str -   If unspecified, loads from "../data/".
    '''
            
    if path is None:
        path="../data/"
        
    with open(path+filename+".family", "rb") as f:
        file=pickle.load(f)
            
    return file

    
# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 