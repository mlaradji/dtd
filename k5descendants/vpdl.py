#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 11:22:28 2018

@author: mohamed
"""

# =============================================================================
# 
# =============================================================================


import dtrl as dtrl
import examples as examples

from sage.graphs.graph_generators import graphs
from copy import deepcopy


# =============================================================================
# 
# =============================================================================

def vector_form(G):
    
    if G.is_isomorphic(graphs.CompleteGraph(5)):
        return tuple([tuple([3]),tuple()])
    if dtrl.is_one_zigzag(G):
        return tuple([tuple([G.order()-2]),tuple()])
    
    K=pd_relabel(G)
    
    #This piece of code constructs an ordered list of edges that are not
    # in chains. These will be the "chords" in our graph.
    #
    
    chainlist,chainvertexlist=dtrl.list_chains(K)
    #chainlist,chainvertexlist=orderchainlist(chainlist,chainvertexlist)
    chainedgelist=[]
    lonevertices=deepcopy(K.vertices())
    for chain in iter(chainvertexlist):
        for zigzag in iter(chain):
            chainedgelist.extend(K.subgraph(zigzag).edges())
            for i in range(0,len(zigzag)):
                try:
                    lonevertices.remove(zigzag[i])
                except:
                    continue
                    
    H=deepcopy(K)
    H.delete_edges(chainedgelist)
    E=deepcopy(H.edges())
    
    position=vertex_positions(H,chainvertexlist,lonevertices)
    #print(position)
    poc=dict() #positions of chords
    
    for i in range(0,len(E)):
        u,v=E[i][0],E[i][1]
        pos1 = next(key for key, value in position.items() if u in set(value))
        pos2 = next(key for key, value in position.items() if v in set(value))
        poc[i]=[pos1,pos2]
    
    chordlengthvector=tuple([abs(poc[i][1]-poc[i][0]) for i in range(0,len(E))])
    chainv=chain_vector(chainlist,len(lonevertices))
    
    return chainv,chordlengthvector

# =============================================================================
# relabel(Graph)-> Graph
# relabel takes a pseudo-descendant graph and relabels it in order of its chain
# list.
#
# This function needs updating.
# =============================================================================

def pd_relabel(G,outputcolor=0,colorlist=0):
    
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
# 
# =============================================================================


def chain_vector(chainlist,lvcount):
    cv=[]
    cond0=(len(chainlist)==1 and lvcount==0)
    
    for chain in iter(chainlist):                   
        for Z in iter(chain):
            cv.append(Z)
        if not cond0:
            cv.append(0)
    
    if lvcount>0:
        cv.append(-lvcount)
        
    return tuple(cv)


#######################################################################

def vertex_positions(G,chainvertexlist,lvlist):
    positionindex=0
    position=dict()

    for chain in iter(chainvertexlist):
        for zigzg in iter(chain):
            if len(chain)==1:
                zigzag=sorted(zigzg)
            else:
                zigzag=zigzg
            for i in range(0,len(zigzag)): 
                if G.degree(zigzag[i])==2:
                    position[positionindex]=[zigzag[i]]
                    positionindex+=1
                elif G.degree(zigzag[i])==1:
                    if len(zigzag)==4:
                        if positionindex not in position:
                            position[positionindex]=[zigzag[i]]
                        else:
                            position[positionindex].append(zigzag[i])
                            positionindex+=1
                    else:
                        position[positionindex]=[zigzag[i]]
                        positionindex+=1
                        
    if len(lvlist)>0:
        vertex=lvlist[0]
        l=-len(lvlist)
        while l<0:
            position[positionindex]=[vertex]
            positionindex+=1
            vertex+=1
            l+=1                    
    
    return position

# =============================================================================
# function ncztl(G): Graph -> integer, integer, integer, integer, integer
#
# This function takes a graph (assumed to be a pseudo-descendant that is not K5 or its first child)
#   and outputs the following "pseudo-descendant quantities" (in order):
#
#       - number of vertices (n),
#       - number of open chains (c),
#       - number of zigzags (z),
#       - number of triangles (t),
#       - number of lone vertices (l).
#
# Note that, for a pseudo-descendant, Proposition 4.19 of the thesis guarantees that
#   n=c+z+t+l.
#
#
# 
# Example: > ncztl((2,2))   
#          > ()
# =============================================================================


def nlcz(G):
    #n,l,c,z: number of vertices, level, number of open chains, number of zigzags
    if dtrl.is_one_zigzag(G):
        return tuple([G.order(),G.order()-G.triangles_count(),0,1])
    
    chain_vector, chord_vector=vector_form(G)
    n=G.order()
    l=n-G.triangles_count()
    c,z=0,0

    if not len(chord_vector)==0: #Check if G is a 1-zigzag.
        for zigzag in iter(chain_vector):
            if zigzag==0:   # zigzag=0 indicates that the (open) end of a chain has been reached.
                c+=1
            elif zigzag>0:  # zigzag=m>0 is a proper zigzag with m triangles (if it is not a 1-zigzag).
                z+=1
    
    return n,l,c,z