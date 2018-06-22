#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon June  18 12:26:28 2018

@author: mohamed
"""

# =============================================================================
# 
# =============================================================================


import dtrl as dtrl
import vpdl as vpdl
import examples as examples

import time as time
import pickle as pickle
import itertools as itertools
from collections import OrderedDict as OrderedDict

from copy import deepcopy

from sage.graphs.graph_generators import graphs
from sage.rings.finite_rings.integer_mod import mod


# =============================================================================
# Function element_sum(vector): list -> integer
#
#   This function simply sums the values inside a list.
# =============================================================================

def vector_sum(vector):
    total=0
    for element in iter(vector):
        total+=element
    return total


# =============================================================================
# Function vector_lt_lex(vector1,vector2,reverse): tuple, tuple, bool -> bool
#
#   This function returns the greater of vector1 and vector2 in the lexicograp-
#       -hical ordering. If vector1 and vector2 are of different lengths, 0's 
#       are appended to the shorter one from the left until they are of equal 
#       length.
# =============================================================================

def vector_lt_lex(vector1,vector2,reverse=False):
    
    v1,v2=list(vector1),list(vector2)
    
    #Resize both vectors to the same lengths.
        
    if reverse:
        v1=list(reversed(v1))
        v2=list(reversed(v2))
        
    while len(v1)<len(v2):
        v1.append(0)
    while len(v1)>len(v2):
        v2.append(0)
        
    for i in range(0,len(v1)):
        if v1[i]<v2[i]:
            return 1
        elif v1[i]>v2[i]:
            return 0
    return 0

    
# =============================================================================
# Function vector_lt(vector1,vector2,ordering,reverse): tuple, tuple, string,
#           bool -> bool
#
#   This function returns 1 if vector1<vector2, and 0 otherwise.
#
#   Supported orderings:
#       - Lexicographical ordering ('lex')
#       - Graded lexicographical ordering ('grlex')
#       - Reverse of either. Use reverse=True.
# =============================================================================

def vector_lt(vector1,vector2,ordering='lex',reverse=False):
        
    if ordering=='lex':
        return vector_lt_lex(vector1,vector2,reverse)
    
    if ordering=='grlex':
        v1sum,v2sum=vector_sum(vector1),vector_sum(vector2)
        if v1sum<v2sum:
            return 1
        if v1sum>v2sum:
            return 0
        
        return vector_lt_lex(vector1,vector2,reverse)

    
# =============================================================================
# Function cyclic_permutations(length): +ve integer -> generator
# 
#   Produces an iterable of a cyclic permutation of length "length".
# =============================================================================

def cyclic_permutations(length):
    S=[i for i in range(0,length)]
    index=0
    while 1:
        yield S
        index+=1
        if index==length:
            raise StopIteration
        S=[S[mod(i+1,length)] for i in range(0,length)]
        

# =============================================================================
# Function chain_permutations(length_list): list of integers -> generator
# 
#   Produces an iterable of permutations of (1,..,n) for n in length_list.
# =============================================================================        
        
def chain_permutations(lengthlist):
    P=[itertools.permutations(range(0,lengthlist[i])) for i in range(
        0,len(lengthlist))]
    CP=[P[i].next() for i in range(0,len(P))]
    index=0
    found=0
    while 1:
        yield CP
        while not found:
            try:
                CP[index]=P[index].next()
                found=1
            except StopIteration:
                P[index]=itertools.permutations(range(0,lengthlist[
                    index]))
                CP[index]=P[index].next()
                index+=1
                if index==len(lengthlist):
                    raise StopIteration
        found=0
        index=0

        
# =============================================================================
# Function permutation_lengths(chain_list, chain_vertices):
#   list, list -> list
#
#   This function computes the degrees of freedom in permuting each chain. More
#       specifically, in addition to permuting the chains around, chains with
#       more than one vertex can also be reversed. Let PL be the output of the
#       function for some input of length n. PL[0:n] is list of 2's and 1's,
#       indicating which chains can be reversed. PL[n]=n, which indicates the
#       number of positions that can be permuted.
#
#   Example:
#       permutation_lengths([[2], [2], [0], [0]], [[[1, 5, 8, 7]], [[2, 4, 9, 3]], [[0]], [[6]]])
#       >> [2, 2, 1, 1, 4]
# =============================================================================

def permutation_lengths(chain_list, chain_vertices):
    
    # It does not seem necessary to use both chain_list and chain_vertices.
    
    lengths_list=[]
    
    if len(chain_list)==len(chain_vertices):
        
        for chain in iter(chain_list):
            if chain[0]>0:
                lengths_list.append(2)
            else:
                lengths_list.append(1)
                
        lengths_list.append(len(chain_list))
            
    else:
        raise ValueError('chain_list and chain_vertices must be of the same length.')
    
    return lengths_list   


# =============================================================================
# Function permute_chains(chain_list, chain_vertices, permutation):
#   list, list, list -> list, list
#
#   This function permutes the chains using permutation.
# =============================================================================

def permute_chains(chain_list, chain_vertices, permutation):

    new_chain_list, new_chain_vertices=[],[]
    
    if len(chain_list)==len(chain_vertices) and len(chain_list)==len(permutation):
        for i in range(0,len(permutation)):
            new_chain_list.append(chain_list[permutation[i]])
            new_chain_vertices.append(chain_vertices[permutation[i]])
            
    else:
        raise ValueError('chain_list, chain_vertices, and permutation must be of the same length.')
    
    
    return new_chain_list, new_chain_vertices


# =============================================================================
# Function collapse_list(list): list -> list
#
#   This function collapses a list of lists into one list. Currently, this only
#       works for the chain_vertices list in the format that is output by 
#       dtrl.list_chains(). That is, this function currently takes a twice ne-
#       -sted list (e.g. [[[1, 5, 8, 7]], [[2, 4, 9, 3]], [[0]], [[6]]]) and o-
#       -utputs the elements (e.g. [1,5,8,7,2,4,9,3,0,6]).
#
#   Though it does not seem necessary to its current use, it might be worthwhi-
#   -le coding a more general function.
# =============================================================================

def flatten_list(big_list, remove_duplicates=True, nest_level=2):
    flattened_list=[]
    
    for small_list in iter(big_list):
        for smaller_list in iter(small_list):
            
            if nest_level==2:
                for element in iter(smaller_list):
                
                    flattened_list.append(element)
            
            elif nest_level==1:
                flattened_list.append(smaller_list)
            else:
                raise ValueError('Only nest_level \in {1,2} has been implemented.')
                
    if remove_duplicates:
        # The following line was obtained from user 'poke' in Stack Overflow 
        #(https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists)
        flattened_list=list(OrderedDict.fromkeys(flattened_list))
    
    return flattened_list
        

# =============================================================================
# Function reverse_chain(chain): list -> list
#
#   This function takes a list of lists (e.g. [[2,1],[1,4]]), and reverses it
#       (e.g to [[4,1],[1,2]]).
# =============================================================================

def reverse_chain(chain):
    
    reversed_chain=list(reversed(chain))
    for i in range(0,len(reversed_chain)):
        reversed_chain[i]=list(reversed(reversed_chain[i]))
        
    return reversed_chain


# =============================================================================
# Function minimal_vector(G,ordering,maximal): graph, string, bool -> tuple, tuple
#
# This function takes a graph, assumed to be a pseudodescendant, and outputs
#   the vector form that has minimal chord length vector wrt the chosen orderi-
#   -ng. Currently supported orderings are 'lex' and 'grlex'. If maximal=True,
#   this function returns the maximal vector instead of the minimal one. If
#   reverse=True, the ordering is reversed so that, for instance, (2,1,1)<(1,1,2)
#   instead of the default (2,1,1)>(1,1,2).
# =============================================================================

def minimal_vector(G,ordering='grlex',reverse=False,maximal=False,verbose=0):

    if G.is_isomorphic(graphs.CompleteGraph(5)):
        return tuple([tuple([3]),tuple([0])]) 
                        # Though there are no chords, tuple(0) is used here to be
                        #   able to index these graphs by their chord length vectors.
                        # There should be no confusion as the chord length vectors
                        #   should never contain 0's.
            
    if dtrl.is_one_zigzag(G):
        return tuple([tuple([G.order()-2]),tuple([0])]) 
    
    chain_list,chain_vertices_list=deepcopy(dtrl.list_chains(G,lone_vertices=True))
    min_clv=chord_length_vector(G,chain_list,chain_vertices_list)
    min_chain_list=deepcopy(chain_list)
    min_chain_vertices_list=deepcopy(chain_vertices_list)
    n=len(chain_list)
    
    for permutation in chain_permutations(permutation_lengths(chain_list,chain_vertices_list)):
                
        new_chain_vertices_list=[]
        # The chains are reversed according to permutation[0:n].
        for i in range(0,n):
            if permutation[i][0]: 
                new_chain_vertices_list.append(deepcopy(reverse_chain(chain_vertices_list[i])))
                
            else:
                new_chain_vertices_list.append(deepcopy(chain_vertices_list[i]))
                
                # Using permutations to indicate reversals is unnecessary.
                # It shouldn't have any effect on performance though. 
        #print(new_chain_vertices_list)
        #print(chain_vertices_list)
        #print(chain_list)
        
        # The chains are permutated. Recall that permutation[n] is a permutation of (0,1,...,n-1).
        new_chain_list, new_chain_vertices_list=permute_chains(chain_list,new_chain_vertices_list, permutation[n])
        #if verbose>=2: print(new_chain_list)
        #if verbose>=2: print(new_chain_vertices_list)
        
        # G will be reordered according to the new order of the chains.
        vertex=flatten_list(new_chain_vertices_list)
        vertex_labels=dict()
        
        for i in range(0,len(vertex)):
            vertex_labels[vertex[i]]=i

        if verbose>=2: print(vertex_labels)
        
        H=deepcopy(G)
        H.relabel(vertex_labels)
        
        #   The following code relabels the vertices in new_chain_vertices_list for consistency.
        new_chain_vertices_list=deepcopy(new_chain_vertices_list)
        for i in range(0,len(new_chain_vertices_list)):
            for j in range(0,len(new_chain_vertices_list[i])):
                for k in range(0,len(new_chain_vertices_list[i][j])):
                    new_chain_vertices_list[i][j][k]=vertex_labels[new_chain_vertices_list[i][j][k]]
                
        if verbose>=2: print('minimal_vector: '+str(chain_vertices_list))

        # Now, the chord length vector will be calculated for the new ordering.
        new_clv=chord_length_vector(H,new_chain_list,new_chain_vertices_list,verbose=0)
        
        
        # The new clv and min clv will be compared.
        lt=vector_lt(new_clv,min_clv,ordering,reverse)
        if lt or (maximal and (not lt) and new_clv!=min_clv):
            min_clv=new_clv
            min_chain_list=new_chain_list
            min_chain_vertices_list=new_chain_vertices_list
            #new_clv=chord_length_vector(G,new_chain_list,new_chain_vertices_list,verbose=3)
    
    is_nzigzag=len(min_clv)==len(min_chain_list)
    
    if verbose>=1: print(min_chain_list)
    if verbose>=1: print(min_chain_vertices_list)
    
    return tuple([tuple(chain_vector(min_chain_list,is_nzigzag)),tuple(min_clv)])
            
        

# =============================================================================
# function chord_length_vector(G,chain_list,chain_vertex_list): 
#       graph, tuple -> tuple
#   
#   This function takes a graph and an associated chain_list,chain_vertex_list, 
#       and attempts to calculate the chord length vector.
# =============================================================================

def chord_length_vector(G,chain_list,chain_vertex_list,verbose=0):
    
    if G.is_isomorphic(graphs.CompleteGraph(5)):
        return tuple(0) # Though there are no chords, tuple(0) is used here to be
                        #   able to index these graphs by their chord length vectors.
                        # There should be no confusion as the chord length vectors
                        #   should never contain 0's.
            
    if dtrl.is_one_zigzag(G):
        return tuple(0)
    
    #The following piece of code constructs an ordered list of edges that are not
    # in chains. These will be the "chords" in our graph.
    #
    
    K=deepcopy(G)
    
    chain_edges,chord_edges=[],[]

    for chain in iter(chain_vertex_list):
        for zigzag in iter(chain):
            chain_edges.extend(K.subgraph(zigzag).edges())
                    
    K.delete_edges(chain_edges)
    chord_edges=K.edges()
    
    # The following code calculates the 'lengths' of the chord edges.
    #print(chain_vertex_list)
    position=vertex_positions(G,chain_vertex_list)

    poc=dict() #positions of chords
    
    E=chord_edges
    if verbose>=3: 
        print(position)
        #print(E)
        #print(chain_vertex_list)
    
    for i in range(0,len(E)):
        u,v=E[i][0],E[i][1]
        pos1 = next(key for key, value in position.items() if u in set(value))
        pos2 = next(key for key, value in position.items() if v in set(value))
        poc[i]=[pos1,pos2]

    
    clv=tuple([abs(poc[i][1]-poc[i][0]) for i in range(0,len(E))])
    # clv: chord length vector
    
    return clv


# =============================================================================
# function vertex_positions(G,chain_vertex_list): graph, list -> dict
#   
#   This function takes a graph and an associated chain_vertex_list, and outputs
#       a dictionary of vertex 'positions'. It is assumed that chain_vertex_list
#       contains lone vertices.
#
# =============================================================================

def vertex_positions(G,chain_vertex_list,reverse=False,verbose=0):
        
    position_index=0
    position=dict()

    for chain in iter(chain_vertex_list):
        
        #print(chain)
        
        chain_vertices=flatten_list(chain,nest_level=1)
        H=G.subgraph(chain_vertices)
        
        
        if len(chain_vertices)>1:
            for vertex in iter(chain_vertices):
            
                deg=H.degree(vertex)

            
                if deg==2 or deg==3:      #This means vertex is a chord vertex or an end vertex.
                    
                    if reverse:
                        position[vertex]=position_index
                    else:
                        position[position_index]=[vertex]
                    position_index+=1
                    
        else: # This means chain is just a lone vertex.
            vertex=chain_vertices[0]
            
            if reverse:
                position[vertex]=position_index
            else:
                position[position_index]=[vertex]
            position_index+=1
            
        if verbose>1: print('vertex_positions: '+str(chain_vertex_list))
    return position


# =============================================================================
# relabel(Graph)-> Graph
# relabel takes a pseudo-descendant graph and relabels it in order of its chain
# list.
#
# This function needs updating.
# =============================================================================

def pd_relabel(G,color_output=False,color_list=None):
    
    # If G is a 1-zigzag graph, pd_relabel will simply return the 1-zigzag with 
    #   the same number of vertices, using the fact that there is exactly one 
    #   1-zigzag for each order.
    
    if dtrl.is_zigzag(G):
        return examples.one_zigzag(G.order()-2)
    
    
    chainlist,chainvertexlist=dtrl.list_chains(G)
    #chainvertexlist,chainlist=orderchainlist(chainvertexlist,chainlist)
    
    #H=deepcopy(G)
    K=deepcopy(G)
    lv=K.vertices()  # lv - (eventually) list of lone vertices
    index=0
    colorindex=0
    label=dict()
    color=dict()
    rcolor=dict()
    
    if not colorlist:
        colorlist=['blue', 'green', 'red', 'cyan', 'm', 'yellow',
                   'black', 'white']
    
    for chain in iter(chainvertexlist):
        for zigzag in iter(chain):

            for i in range(0,len(zigzag)):
                if not zigzag[i] in label:
                    label[zigzag[i]]=index
                    rcolor[index]=colorlist[colorindex]
                    if colorlist[colorindex] in color:
                        color[colorlist[colorindex]].append(index)
                    else:
                        color[colorlist[colorindex]]=[index]
                    index+=1
                    lv.remove(zigzag[i])
            colorindex+=1
            
    for vertex in iter(lv):
        label[vertex]=index
        rcolor[index]=colorlist[colorindex]
        color[colorlist[colorindex]]=[index]
        index+=1
        colorindex+=1
        
    K.relabel(label)
    
    if outputcolor:
        return K,color,rcolor
    else:
        return K
    
    
# =============================================================================
# function chain_vector(chain_list): list -> tuple
#
#   This function takes a chain_list as output by dtrl.list_chains(G,lone_vertices=True)
#       and output a single list.
#
#   Example:    L=dtrl.list_chains(G,lone_vertices=True)
#               print(L)
#               >>> [[[1, 5, 8, 7]], [[2, 4, 9, 3]], [[0]], [[6]]]
#               co.chain_vector(chain_list)
#               >>> (2,0,2,0,-1,-1)
# =============================================================================


def chain_vector(chain_list,is_nzigzag=False):
    
    chain_vect=[]   #chain_vector
    
    for chain in iter(chain_list):                   
        for zigzag in iter(chain):
            if zigzag>0:
                chain_vect.append(zigzag)
            elif zigzag==0:
                chain_vect.append(-1)
        if (not is_nzigzag):
            chain_vect.append(0)
        
        
    return tuple(chain_vect)