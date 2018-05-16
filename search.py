#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 15:07:28 2018

@author: mohamed
"""

# =============================================================================
# 
# =============================================================================


import dtrl as dtrl
import vpdl as vpdl
import examples as examples

from copy import deepcopy
from sage.graphs.graph_generators import graphs
import time as time
import pickle

# =============================================================================
# Function descendant_search(parents, family, max_level, print_time):
#   list, dict, integer, bool -> None
#
# parents - list of graphs to calculate the descendants of.
#
# family - dictionary of descendants. Note that the function operates and changes
#   this dictionary, so keep a backup.
#
# max_level - if None, all descendants are calculated. Otherwise, all descendants of
#   level<=max_level are calculated. If only a certain level is desired, setting this
#   option to a positive integer could greatly speed up the calculation.
#
# print_time - True or False - set to False to stop printing of time elapsed.
# =============================================================================

def descendant_search(family=list(), max_order=None, max_level=None, initialize=False, savefile=True, savename='descendants', print_time=True):
    
    start_time = time.time()
    
    if initialize:                          # Set initialize=True to start the search with K5.
        G=graphs.CompleteGraph(5)
        n,L,c,z=list(vpdl.nlcz(G))              # vpdl.nlcz(G)->n,L,c,z (number of vertices, level, no. of
                                            #   open chains, number of zigzags)
        
        while len(family)<n+1:
            family.append([])
            
        family[5].append([[[[G,vpdl.vector_form(G),[0,0,0,0]]]]])
        
        # family[5][0][0][0][0] is K5 (Technically, Level(K5)=-5.)
    
    no_max_order=False  # no_max_order is set to True if max_order=None.
    
    if max_order==None:
        max_order=1
        no_max_order=True
    
    for order in range(0,max_order):
        
        if no_max_order:
            max_order+=1
        
        int_time, nc_time=time.time(),time.time()
        
        if len(family)<order+1:
            family.append([])
        
        for level in range(0,len(family[order])):
            for chno in range(0,len(family[order][level])):
                for zgno in range(0,len(family[order][level][chno])):
                    for index in range(0,len(family[order][level][chno][zgno])):
                                                
                        # chno - number of open chains
                        # zgno - number of zigzags
                        # Indexing graphs by their chno and zgno can hasten the isomorphism check, which is by far
                        #   the slowest part of this algorithm.
                        
                        G=deepcopy(family[order][level][chno][zgno][index])
                        
                        # G[0] - graph form. G[1] - vector form (not unique). G[2] - expanded triangles.
                        
                        triangles_list=dtrl.list_triangles(G[0])       
                        
                        # dtrl.list_triangles(G) partitions the triangles in G
                        #   according to their triangle type.
        
                        triangles_set=set()   
            
                        # triangles_set will be the set of triangles to be expanded. This will be determined
                        #   based on the max_level setting. If max_level=None, then all triangles will be
                        #   included in triangles_set.
        
                        if max_level==None or level<max_level-1:
                            for i in range(0,4):
                                if not G[2][i]:
                                    triangles_set=triangles_set.union(triangles_list[i])
                            expanded=[1,1,1,1]      
                            
                        # The expanded list will be used to determine which triangle types have been exhausted.
        
                        elif level>max_level:
                            triangles_set=set()
                            expanded=[0,0,0,0]
                
                        elif level==max_level:
                            if not G[2][3]:
                                triangles_set=triangles_list[3]
                            expanded=[0,0,0,1]
            
                        elif level==max_level-1:
                            triangles_set=set()
                            for i in range(1,4):
                                if not G[2][i]:
                                    triangles_set=triangles_set.union(triangles_list[i])
                            expanded=[0,1,1,1]
        
        
                        # Now, we iterate over triangles in triangles_set to produce the desired descendants.
        
                        for triangle in triangles_set:
                
                            H=[]
                            H.append(dtrl.double_triangle_expansion(G[0],triangle))
                            
                            try:
                                n,L,c,z=list(vpdl.nlcz(H[0]))
                            except IndexError:
                                print('An IndexError occurred in trying to evaluate vpdl.nlcz(H[0]).')
                                print('Use H=search.descendant_search() to get hold of the culprit graph.')
                                return H
                            
                            if L<0:
                                L=0

                            while len(family)<n+1:
                                family.append([])
                            while len(family[n])<L+1:
                                family[n].append([])
                            while len(family[n][L])<c+1:
                                family[n][L].append([])
                            while len(family[n][L][c])<z+1:
                                family[n][L][c].append([])
                            
                            # The above piece of code elongates the family list to the right size.
                            
                            iso=0
                            
                            for i in range(0,len(family[n][L][c][z])):
                                if H[0].is_isomorphic(family[n][L][c][z][i][0]):
                                    iso=1
                                    break
                            
                            if not iso:
                                family[n][L][c][z].append([H[0],vpdl.vector_form(H[0]),[0,0,0,0]])
                                
                        # In the following we use the already constructed expanded to take note
                        #    that we have exhausted some of the triangle types in the parent graph G.
                        
                        for i in range(0,4):
                            if expanded[i]:
                                family[order][level][chno][zgno][index][2][i]=1
        
        if savefile:
            save(family,savename,order)
        
        if print_time:
            print(str(order)+'-'+str(time.time() - int_time))
    if print_time:
        print("--- %s seconds ---" % (time.time() - start_time))
        
    return

# =============================================================================
# Function save(family,savename,version):
#   object, string, number -> None
#
# This function saves the object family as savename+str(version)+".file". For
#   instance, if savename='descendants' and version=5, family is saved as
#   descendants5.file.
# =============================================================================

def save(family,savename,version):
    
    with open(savename+"_"+str(version)+".file", "wb") as f:
        pickle.dump(family, f, pickle.HIGHEST_PROTOCOL)
    
    return

# =============================================================================
# Function load(family,savename,version):
#   object, string, number -> None
#
# This function loads the object contained in savename+"_"+str(version)+".file",
#   and saves it in the variable family. For instance, if savename='descendants' 
#   and version=5, the file descendants5.file is loaded as family.
#
# Note that if the variable family was already in memory, all unsaved data will
#   be lost.
# =============================================================================

def load(family,savename,version):
    
    with open(savename+"_"+str(version)+".file", "rb") as f:
        family = pickle.load(f)
    
    return

# =============================================================================
# Function enumerate(family,order=True,)
#   object, string, number -> None
#
# This function loads the object contained in savename+"_"+str(version)+".file",
#   and saves it in the variable family. For instance, if savename='descendants' 
#   and version=5, the file descendants5.file is loaded as family.
#
# Note that if the variable family was already in memory, all unsaved data will
#   be lost.
# =============================================================================

#def enumerate(family,nest_level=None, labels=['order','level','chain count','zigzag count']):
    
   # explored_level=-1
   # nested_family
    
   # while explored_level<nest_level:
   #     for i in range(0,len(nested_family))
    #        a
   #         
   # return