#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 17:34:42 2018

@author: mohamed
"""

# =============================================================================
#
# =============================================================================

#from Zigzag import Zigzag
from Chain import *
from LoneVertex import *
from ChordVector import *
from Complex import *

from common import exceptions
from common import graphs as g

import convert_Graph_to_Pseudodescendant as cgpd

from sage.graphs.graph import Graph
from copy import copy
#import time  


# =============================================================================
#
# =============================================================================

global current_version
current_version='PD_0.1'

class Pseudodescendant(Complex):
    '''
    # class Pseudodescendant.
    #
    #   This class aims to group useful tools for dealing with pseudodescendant objects.
    #   
    #   Recall that a pseudodescendent is graph that has a vector representation.
    # 
    #   Example:   
    #
    '''
    
    type = 'Pseudodescendant'      # class variable shared by all instances

    def __init__(self, chain_vector=None, chord_vector=None, parts=None, 
                 starting_vertex=None, graph=None):
        
        global current_version
        self.version=current_version
        
        chord_edges=None
        self.chord_vector=ChordVector(parent_object=self)
        
        self.same_first_and_last_vertex=False
        
        if graph is None:
            if starting_vertex is None: starting_vertex=0
        
            if parts is None:
                if chain_vector is None: chain_vector=[1]
                self.make_parts(chain_vector=chain_vector)
            
            else: self.make_parts(parts=parts)
            
        else:
            if type(graph) is Graph:
                parts=cgpd.make_parts(graph)
                self.make_parts(parts=parts)
                chord_edges=self.graph_difference(graph, reverse_positions=True)
                
            else: raise TypeError('graph ('+str(graph)+') must be a Graph object.')

        #if chord_vector is None: chord_vector=tuple([])
            
        self.set_chord_vector(chord_vector, chord_edges=chord_edges)
            
    def make_parts(self, chain_vector=None, parts=None, verbose=0):
        
        # If chain_vector is set, make_parts creates the parts from this chain
        #   vector. If parts is set, make_parts simply appends the members of
        #   parts to self.parts.
        
        self.parts=[]
        
        if parts is not None:

            for part in iter(parts):
                
                if verbose>0: print('part: '+str(part))

                part.set_parent_object(self)
                self.parts.append(part)
                
                if verbose>0: print('self.parts: '+str(self.parts))
                    
            return
            
        if chain_vector is None: chain_vector=self.chain_vector()    
        
        broken_chain_vector, no_breaks=break_chain_vector(chain_vector, return_no_breaks=True)
        
        for vector in iter(broken_chain_vector):
            
            if vector==[-1]:  # This means its a lone vertex.
                self.parts.append(LoneVertex())
            
            else:   # This means its a chain.
                chain=Chain(vector,closed=no_breaks)
                self.parts.append(chain)
        
        self.reindex()
        
        return
    
    
    def chain_vector(self):
        
        chain_vector=[]
        #first_chain=True
        
        for part in self.part_iterator():
            #if not first_chain: pass; #chain_vector.append(0)
            #else: first_chain=False
            chain_vector.extend(part.chain_vector())
               
        return tuple(chain_vector)
    
    def part_iterator(self): return iter(self.parts)
    
    def order(self):
        order=0
        
        for part in self.part_iterator():
            order+=part.order()
            
        return order
    
    def triangles_count(self):
        
        triangles_count=0
        
        for part in self.part_iterator():
            triangles_count+=part.triangles_count()
            
        return triangles_count
    
    def rearrange(self, permutation, reorientation=None):
        '''
        # This function rearranges the parts of self according to permutation and
        #   reorientation. 
        '''
        
        if reorientation is not None: reorientation_defined=True
        if permutation is not None: permutation_defined=True
        
        parts=[]
        for i in range(0,len(self.parts)):
            
            if permutation_defined: new_i=permutation[i]
            else: new_i=i
            
            part=self.parts[new_i]
            
            if reorientation_defined and reorientation[new_i]<0: part=part.reverse()
            
            parts.append(part)

        return
            
    
# =============================================================================
# Function self.ncztl():   Pseudodescendant -> List
#
# Calculates the ncztl parameters for the Pseudodescendant object.
#

# =============================================================================

    def ncztl(self, verbose=0):
        '''
        #   Lists the n,c,z,t,l parameters for the pseudodescendant.
        #
        #   The parameters are:
        #       n:  order
        #       c:  open chain count,
        #       z:  (proper) zigzag count,
        #       t:  triangles count,
        #       l:  lone vertex count.
        #
        #   Examples:   G=Pseudodescendant((3,3,0,2,1,3,0,-1,0,-1))
        #               G.ncztl()
        #               >>> (21,2,5,12,2)
        #               H=Pseudodescendant((3))
        #               H.ncztl()
        #               >>> (5,0,1,10,0)
        '''
        
        chain_vector, chord_vector=self.vector_pair()

        n_zigzag=self.is_n_zigzag() 
        # is_n_zigzag=n if self is an n-zigzag, and to 0 otherwise.
        
        if verbose: print('is_n_zigzag :'+str(n_zigzag))
        
        if n_zigzag==1:
            n, c, z, t, l = chain_vector[0]+2, 0, 1, g.triangles_count_Z(chain_vector[0]), 0  
        elif n_zigzag>1:
            c, z, t, l = 0, n_zigzag, sum(chain_vector), 0
            n=c+z+t+l
        else:
            c,z,t,l=0,0,0,0
            new_chain=True
            
            for zigzag in iter(chain_vector):
                if zigzag>0:
                    if new_chain: c+=1;
                    z+=1
                    t+=zigzag
                    
                    new_chain=False
                
                elif zigzag==0: new_chain=True
                
                else: l+=-zigzag
        
            n=c+z+t+l
            
        return tuple([n,c,z,t,l])
    
#    def chord_length_vector(self):
#        return self.vector[1]
        
#    def graph(self):
#        return vrep.graph_form(self.vector)
    
#    def skeleton(self):
#        return vrep.skeleton(self.vector[0])
        
#    def ncztl(self):
#        return vrep.ncztl(self.vector)
    
#    def open_chain_count(self):
#        return self.ncztl[1]
    
#    def zigzags_count(self):
#        return self.ncztl[2]
    
#    def triangles_count(self):
#        return self.ncztl[3]
    
#    def lone_vertices_count(self):
#        return self.ncztl[4]
    
#    def level(self):
#        n,c,z,t,l=self.ncztl
#        return n-t
        
#    def is_n_zigzag(self):
#        return vrep.is_n_zigzag(self.vector)
    
#    def classify_chains(self):
#        return vrep.classify_chains(self.vector[0])
    


def break_chain_vector(chain_vector, return_no_breaks=False):
   '''
   # Function break_chain_vector(chain_vector): list -> list
   #
   #   This function takes a chain vector and breaks it up into smaller parts, 
   #       with each part being a chain vector for an open chain or a lone vertex.
   #
   #    Options:
   #        return_no_breaks - bool - return the number of breaks.
   #
   #    Examples:      
   #       cv=(2,0,-1,0,-1,0,2,0)
   #       break_chain_vector(cv)
   #       >>> [[2],[-1],[-1],[2]]
   #
   #       cv=(2,2,0,-1,0)
   #       break_chain_vector(cv)
   #       >>> [[2,2],[-1]]
   #        
   #       cv=[1,2,0,2,2,-1,2,3,0,-1,-1]
   #       break_chain_vector(cv)
   #       >>> [[1, 2], [2, 2], [-1], [2, 3], [-1], [-1]]
   '''
    
    #vertex_index=-1
    #chain_vertices=[]
    #chain_zigzag_list=[]
    broken_chain_vector=[]
    same_chain=False
    
    no_breaks=True
    # no_breaks indicates whether the chain_vector contains any 0's or -1's. 
    #   If no_breaks, this means that the chain is closed.
    
    for triangles_count in iter(chain_vector):
 
        if triangles_count>0:
            
            if same_chain:
                broken_chain_vector[-1].append(triangles_count)   
            else:
                broken_chain_vector.append([triangles_count]) 
                
            same_chain=True
        
        elif triangles_count==0:
            same_chain=False
            no_breaks=False
        
        elif triangles_count==-1:
            broken_chain_vector.append([-1])
            same_chain=False    # This line might not be necessary.
            no_breaks=False
        
        else:
            raise ValueError('Dealing with values less than -1 in the chain '
                             'vector has not been implemented yet.')
    
    if return_no_breaks:
        return broken_chain_vector, no_breaks
    else: return broken_chain_vector