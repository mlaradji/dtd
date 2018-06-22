# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 16:49:59 2018

@author: Mohamed Laradji
"""

# =============================================================================
# 
# =============================================================================


from sage.graphs.graph import Graph
from copy import deepcopy

import examples as examples


#==============================================================================
# 
#==============================================================================

def double_triangle_reduction(G,dtriangle,require_proper=1,require_4regular=1):
    # This function takes as input a graph G, and a double
    #   triangle (v1,v2,v3,v4) with (v2,v3) the common edge in G.
    # The output is a graph H that is obtained from G by deleting
    #   the edges (v1,v2),(v2,v3) and (v2,v4), adding the edge (v1,v4), and
    #   identifying the vertices v2 and v3. We require that the double
    #   triangle is not part of a triple triangle.
    # Unless require_proper=0, the double triangle must be proper or an
    #   Improper_DTR exception is raised.
    # If require_4regular=0,
    if require_proper and not is_proper_double_triangle(G,dtriangle):
        raise ValueError('The double-triangle is not proper. If intentional, set require_proper=0 to avoid this message. It might also be necessary to use G.allow_multiple_edges() for a correct double-triangle reduction.')
    elif not is_double_triangle(G,dtriangle):
        raise ValueError('Double-triangle reduction of a non-double-triangle.')
    else:
        v1,v2,v3,v4=dtriangle[0:4]
        H=G.copy()
        H.delete_edges([(v1,v3),(v2,v3),(v3,v4)])
        N=H.neighbors(v3)
        if len(N)==0:
            raise ValueError('Double-triangle reduction of a non-4-regular graph or of a graph with multiple edges. If intentional, set require_4regular=0 to avoid this message.')
        H.add_edges([(v2,v) for v in iter(N)])
        H.add_edge(v1,v4)
        H.delete_vertex(v3)
        # The vertices v2 and v3 are identified as v2.
        return H

# =============================================================================
# function double_triangle_expansion(G,triangle,choice,require_neighbours):
#   Graph, list, integer, bool -> Graph
#
# This function takes as input a graph G and a triangle Tr=(v1,v2,v3) in G.
# 
# The output is a new H obtained from G by double-triangle reduction of Tr, with choice the
#   neighboring vertex of v2 to connect to the new vertex. If choice is not
#   specified, the neighbor of v2 will be random. Note that in the case of
#   4-regular graphs, both choices produce isomorphic graphs.
#
# If the neighboring vertices of Tr[1] are v0,v1,v2 with v1<v2<v3,
#   then choice=i means that vi is the choice. For k5-descendants, choice=0
#   or 1.
#
# Example:
# > triangle=[0,1,2]
# > G=graphs.CompleteGraph(5)
# > H=double_triangle_expansion(G,triangle)
# > H.is_isomorphic(examples.one_zigzag(4))
# > > True
# > G.is_isomorphic(examples.one_zigzag(3))
# > > True
# =============================================================================
    
def double_triangle_expansion(G,triangle,choice=0,require_neighbours=1):

    if not is_triangle(G,triangle):
        raise ValueError('Double-triangle expansion of a non-triangle.')

    # The graph K is used to find the neighbors of Tr[1] after the triangle edges
    #   are removed. This is preferred to simply finding the difference set of
    #   the neighbor sets to allow for double-triangle expansion of graphs with multiple edges.
    K=G.copy()
    K.delete_edges([[triangle[0],triangle[1]],[triangle[1],triangle[2]]])
    N=K.neighbors(triangle[1])
    if require_neighbours and len(N)==0:
        raise ValueError('Double-triangle expansion of a non-4-regular-graph. If intentional, set require_neighbours=0.')

    H=G.copy()
    H.delete_edge(triangle[0],triangle[2])
    H.delete_edge(triangle[1],N[choice])
    vn=max(G.vertices())+1
    #vn here is the new vertex created by the double-triangle expansion. This assumes that the vertex
    #   labels are numbers. This is yet to be tested with other forms of vertex
    #   labels.
    newedges=[[vn,triangle[0]],[vn,triangle[1]],[vn,triangle[2]],[vn,N[choice]]]
    H.add_edges(newedges)

    return H


#==============================================================================
# 
#==============================================================================

def find_double_triangle(G):
    reference_dtriangle=Graph([[0,1],[0,2],[1,2],[1,3],[2,3]]) #A double-triangle.
    for dtriangle in G.subgraph_search_iterator(reference_dtriangle,induced=True):
        if is_proper_double_triangle(G,dtriangle):
            return dtriangle
    return 0

def double_triangle_ancestor(G):
    #This function takes as input a 4-regular graph G with no multiple edges.
    #   The output is the double-triangle ancestor of G, which is the graphs
    #       obtained by successive (proper) double-triangle reductions on G.
    #   Although this could work for non-4-regular multigraphs, it has not
    #       been tested for that purpose.
    H=G.copy()
    A=G.copy()
    ancestor_found=0
    while not ancestor_found:
        dtriangle=find_double_triangle(H)
        if dtriangle:
            A=double_triangle_reduction(H,dtriangle)

        # if A==H, then all of the double-triangles in G are improper, and thus
        #   A is the ancestor.
        if A==H:
            ancestor_found=1
        else:
            H=A.copy()
    return A

def is_k5_descendant(G):
    
    #This function outputs 1 or 0 depending on whether G has K5 as the double
    #   triangle ancestor or not.
    
    K5=graphs.CompleteGraph(5)
    return G.is_regular(4) and K5.is_isomorphic(double_triangle_ancestor(G))
    
    
#==============================================================================
#     
#==============================================================================
    
def is_triangle(G,triangle):
    # checks if the induced subgraph of G on v1,v2,v3 is a triangle.
    if len(triangle)==3:
        H=G.subgraph(triangle)
        return H.is_cycle()
    else:
        return 0
        
        
def is_double_triangle(G,dtriangle):
    # checks if dtriangle[0:4] and dtriangle[1:5] are both triangles in G.
    if len(dtriangle)!=4:
        raise ValueError('The dtriangle (double-triangle) vector must be of length 4.')
    triangle1,triangle2=dtriangle[0:3],dtriangle[1:4]
    return (is_triangle(G,triangle1) and is_triangle(G,triangle2))
    

def is_proper_double_triangle(G,dtriangle):
    # checks if the induced subgraph H of G on dtriangle=(v1,v2,v3,v4) is a proper double
    #   triangle, which means that H is a double triangle that is not part of
    #   a 4-clique or a triple triangle in G. Note that ordering is important:
    #   (v1,v2,v3,v4) is a double triangle if (v1,v2,v3) and (v2,v3,v4) are
    #   triangles.
    if not is_double_triangle(G,dtriangle):
        return 0
    elif G.has_edge(dtriangle[0],dtriangle[3]):
        return 0 #Since this means that the dtriangle is part of a 4-clique.

    N=set(G.neighbors(dtriangle[1])).intersection(set(G.neighbors(dtriangle[2]))).difference(set([dtriangle[0],dtriangle[3]]))
        # N is the set of common neighbors of v2,v3 that are not v1 or v4.
        # If N is not empty, then the double triangle is part of a triple
        #   triangle.

    if len(N)>0:
        return 0
    return 1


def is_one_zigzag(G):
    # checks if G is a 1-zigzag.
    
    n=G.order()
    return G.is_isomorphic(examples.one_zigzag(n-2))


def is_zigzag(G):
    # checks if G is a zigzag.
    
    n=G.order()
    return G.is_isomorphic(examples.zigzag(n))
    
# =============================================================================
#     
# =============================================================================


#==============================================================================
#         
#==============================================================================

def find_triangle(G,v=None):
    H=G.copy() #G is copied here to avoid accidental changes to the original
                  #     original graph.

    # vertices is an iterable of the vertices of G to be searched for triangles.
    if v!=None and H.has_vertex(v):
        vertices=iter([v])
    else:
        vertices=H.vertex_iterator()

    # The neighbors of vi, chosen from the vertices iterable, are searched for
    #   triangles.
    for vi in vertices:
        for vj in H.neighbor_iterator(vi):
            for vk in H.neighbor_iterator(vi):
                if vj!=vk and H.has_edge(vj,vk):
                    return [vi,vj,vk] #The output triangle

    # If this point is reached, then no triangles were found. The function
    #   returns 0.
    return 0

    
def find_zigzag(G,v=None):
    H=G.copy()

    Z=find_triangle(H,v) 
    
    # If Z!=0, then Z=[v1,v2,v3] for some vertices v1,v2,v3 in G. 
    # As the function runs, vertices will be appended to Z until no more 
    #    can be added without making Z a non-zigzag. Z is the unordered 
    #    maximal zigzag. Z_ordered, which is Z ordered in the "standard 
    #    zigzag ordering", is the output of find_zigzag.

    if not Z:
        return 0    # If find_triangle(H,v) returns 0, then G has no triangles,
                    #   and so find_zigzag will return 0, as desired.


    import collections as collections
    
    edges_queue=collections.deque()   
    
    # As Z is expanded, the zigzag edges incident to vertices
    #   added to Z will be removed from the graph H (not the
    #   original graph) and added to the edges_queue deque. This
    #   is done so that find_triangle(H,v) only outputs triangles
    #   that have not been output before, and so that the code
    #   terminates when all triangles have been output.
    #   edges_queue is a deque object containing edges [v1,v2].

    for i in range(0,2):
        for j in range(i+1,3):
            edges_queue.append([Z[i],Z[j]])
            H.delete_edge([Z[i],Z[j]])

    # The following
    #   code iterates over the edges of edges_seen to find a vertex that
    #   is adjacent to both vertices of the current edge, which would
    #   form a new triangle that is part of the current zigzag.

    while len(edges_queue)>0:
        edge=edges_queue.popleft()
        N1=set(H.neighbors(edge[0]))
        N2=set(H.neighbors(edge[1]))
        V=list(N1.intersection(N2))
        # V is a list of vertices that are adjacent to both vertices of the
        #   current edge in edges_seen.

        if len(V)>1:
            raise ValueError('G is not a pseudo-descendant.')
            # If len(V)>1, then G contains a triple triangle and so G is not a
            #   pseudo-descendant. This function only works for pseudo-descendants.

        elif len(V)==1:
            vertex=V[0]
            Z.append(vertex)
            edges_queue.append([vertex,edge[0]])
            edges_queue.append([vertex,edge[1]])
            H.delete_edges([(vertex,edge[0]),(vertex,edge[1])])
            # If V contains only 1 vertex, then this vertex added to the vertices
            #   along with the vertices in Z form a larger zigzag than Z. Hence,
            #   vertex is added to the Z list, and the edges incident to the
            #   to vertex and to edge are added to edges_queue.

        # If len(V)=0, then the zigzag Z cannot be extended using edge.

    # At this point in the code, we have an unordered list, Z, of vertices of a
    #   maximal zigzag of G. The following code orders Z in the
    #   "standard zigzag ordering", producing the list of vertices Z_ordered.
    
    index=0
    
    if len(Z)>3:
        # If len(Z)>3, then the zigzag contains more than one triangle.
        Z_ordered=[]
        zigzag=G.subgraph(Z)
        for i in range(0,len(Z)):
            if zigzag.degree(Z[i])==2:
                Z_ordered.append(Z[i])
                index=0
                N=zigzag.neighbors(Z_ordered[0])
                for i in range(0,len(N)):
                    if zigzag.degree(N[i])==3:
                        Z_ordered.append(N[i])
                        break
                zigzag.delete_edge(Z_ordered)
                break
                # One of the degree 2 vertices is chosen as the starting point.
                
        #print(Z_ordered)
        #if len(Z_ordered)==0:
        #    Z_ordered=find_double_triangle(zigzag)
        #    zigzag.delete_edges(zigzag.subgraph(Z_ordered).edges())
        #    zigzag.delete_vertex(Z_ordered[1])
        #    index=2
            # len(Z_ordered)==0 implies that (the induced subgraph on) Z has no
            #   degree 2 vertices. This means that Z is in fact a 1-zigzag.
            # find_double_triangle is used to "orient" the zigzag. The edges of
            #   the double triangle that is found and one of the 3-valent vertices
            #   (in the double triangle subgraph) are removed so that the
            #   next loop (while zigzag.size()>0:) terminates properly.
            

        # The degree 3 vertex v1 adjacent to the starting vertex v0 is the next in order,
        #   in accordance with the "standard zigzag ordering". The edge
        #   Z_ordered=[v0,v1] is then deleted from the zigzag.
        #print(Z)
        while zigzag.size()>0:
            #print(Z_ordered)
            #print(index)
            N1=set(zigzag.neighbors(Z_ordered[index]))
            N2=set(zigzag.neighbors(Z_ordered[index+1]))
            Nc=list(N1.intersection(N2)) # Nc is the list of common neighbors
                                         #  of the last two seen vertices in
                                         #  Z_ordered. For a pseudo-descendant,
                                         #  Nc must be of length=1, or else
                                         #  G contains a triple triangle.
            #print(Z)
            #print(Z_ordered)
            Z_ordered.append(Nc[0])      #  The common neighbor is added.
            
            e1=(Z_ordered[index],Nc[0])
            e2=(Z_ordered[index+1],Nc[0])
            zigzag.delete_edges([e1,e2])
            # The edges incident to two of the vertices Z_ordered[i], Z_ordered[i+1]
            #   and Nc[0] are deleted from zigzag. Edges will continue to be removed
            #   until zigzag has no more edges left, which means that Z_ordered
            #   contains the desired ordered list of zigzag vertices.

            index+=1

    elif len(Z)==3:
        # If len(Z)==3, then the zigzag contains only one triangle. In the
        #   following code, the vertices in the list Z are permuted so that
        #   vertices which are part of two maximal zigzags in G are at the
        #   beginning or the end of Z_ordered.

        Z_ordered=Z
        if G.cluster_triangles(Z[1])==2:
            Z_ordered=[Z[0],Z[2],Z[1]]

        if v!=Z[0] and G.cluster_triangles(Z[0])==1 and G.cluster_triangles(Z[1])==2:
            Z_ordered=[Z[1],Z[0],Z[2]]

    return Z_ordered
    
    
#==============================================================================
# list_chains(G) creates two lists from G, the first of which is a list
#   of lists (chains) of zigzag lengths. The second list is a list of lists
#   of lists of zigzag vertices, corresponding to the zigzag lengths in the
#   first list. The input graph G is assumed to be pseudo-descendant, and
#   the function has not been tested for other graphs.
#
# Example output: [[3, 3]], [[[0, 6, 7, 4, 1], [1, 5, 8, 2, 3]]]
#
# The function first starts with a zigzag, say Z1, found using find_zigzag(G). 
# There are then two directions to search for more zigzags that are in the same
#   chain as Z1. The function searches in one of these directions (the chosen
#   direction depends on the vertex labels of the graph), and adds zigzags that
#   are found until there are none left. Then, the reverse direction is searched,
#   starting at Z1 again, and zigzags are added until there are no zigzags left.
#   Then, the function attempts to find a new chain, and the process is repeated.
#   This continues to be done until no chains are left.    
#==============================================================================

def list_chains(G, lone_vertices=False):
    H=G.copy()

    reverse_direction=0     # reverse_direction is set to 1 when the right end of
                            #   a chain is reached.

    start_new_chain=1       # start_new_chain is set to 0 when looking for
                            #   zigzags in the same chain, and to 1 when a
                            #   chain is completed.

    chain_list=[]            # chainlist and chainvertices are the output lists
    chain_vertices=[]        #   of list_chains(G).

    while H.triangles_count()>0:    # Triangles are deleted from H as the zigzags
                                    #   are added. No more triangles means no more
                                    #   zigzags, and so the function terminates.

        if start_new_chain:

            Z=find_zigzag(H)
            H.delete_vertices(Z[1:-1])

            # Z[1:-1] are all the vertices of the zigzag except for the degree
            #   2 vertices. Those are not deleted as they may be part of other
            #   zigzags.

            #if A.subgraph(Z).is_regular(4):    #Dont think this is needed
            #    tri=len(Z)

            if Z[0]!=Z[-1]:
                no_of_triangles=len(Z)-2    #no_of_triangles is the number of triangles.
            else:
                no_of_triangles=len(Z)-1

            # If Z[0]==Z[-1], then Z is a 1-zigzag. A 1-zigzag has the same
            #   number of vertices as there are triangles.
            
            chain_list.append([no_of_triangles])

            chain_vertices.append([Z])

            start_new_chain=0

            #current_first_v=Z[0]
            #current_last_v=Z[-1]
            # current_first_v and current_last_v are the middle/end vertices,
            #   the degree 2 vertices, of the current zigzag.

        else:
            if reverse_direction:
                middle_vertex=chain_vertices[-1][0][0]
                Z=find_zigzag(H,middle_vertex)
                # The leftmost (potentially) middle vertex of the current zigzag
                #   is checked for membership in another zigzag.

                if not Z:
                    H.delete_vertex(middle_vertex)
                    # not Z implies that "middle_vertex" is not part of a
                    #   second zigzag, and so it is safe to remove it from H.

                    start_new_chain=1
                    reverse_direction=0
                    # We start a new chain as both the left and right ends of
                    #   the current chain have been checked for zigzags.

                else:
                    if Z[0]==middle_vertex:
                        Z.reverse()

                    no_of_triangles=len(Z)-2
                    chain_list[-1].insert(0,no_of_triangles)
                    chain_vertices[-1].insert(0,Z)
                    H.delete_vertices(Z[1:-1])

            else:
                middle_vertex=chain_vertices[-1][-1][-1]
                Z=find_zigzag(H,middle_vertex)
                #print(Z)
                #print(val)
                #print(A.edges())

                if not Z:
                    H.delete_vertex(middle_vertex)
                    reverse_direction=1
                else:
                    if Z[-1]==middle_vertex:
                        Z.reverse()
                    no_of_triangles=len(Z)-2
                    chain_list[-1].append(no_of_triangles)
                    chain_vertices[-1].append(Z)
                    H.delete_vertices(Z[1:-1])
    
    if lone_vertices:
        for lv in iter(list_lone_vertices(G)):
            chain_list.append([0])
            chain_vertices.append([[lv]])
    
    return chain_list, chain_vertices


#==============================================================================
# list_lonevertices(G): graph -> list
#
# This function lists the non-triangle vertices of G.
#==============================================================================

def list_lone_vertices(G):
    
    lone_vertices=[]
    
    for key, value in G.cluster_triangles().items():
        if value==0:
            lone_vertices.append(key)
    
    return lone_vertices


# =============================================================================
# function list_triangles(G): Graph -> set, set, set
#
# list_triangles finds all triangles in G and partitions them according to the
#   "Triangle Type".  
# =============================================================================

def list_triangles(G):
    
    # This function partitions triangles in G by their triangle type (wrt double triangle expansion),
    #   by iteratively searching the graph G for triangles that are not of the previous types. That is,
    #   to check that a triangle T is of type II, we need to check that it is isomorphic to the graph
    #   triangle_type(2) (which means the triangle is either Type I or Type II) but not to the graph   
    #   triangle_type(1).
    
    H=deepcopy(G)
    S=[set(),set(),set(),set()]
    
    for triangle in H.subgraph_search_iterator(triangle_type(1)):
        triangle_vertices=extract_triangle_vertices(triangle)
        S[0].add(triangle_vertices)
        
    for triangle in H.subgraph_search_iterator(triangle_type(2)):
        triangle_vertices=extract_triangle_vertices(triangle)
        if triangle_vertices not in S[0]:
            S[1].add(triangle_vertices)
            
    for triangle in H.subgraph_search_iterator(triangle_type(3)):
        triangle_vertices=extract_triangle_vertices(triangle)
        if triangle_vertices not in S[0]:
            S[2].add(triangle_vertices)
            
    for triangle in H.subgraph_search_iterator(triangle_type(4)):
        triangle_vertices=extract_triangle_vertices(triangle)
        if triangle_vertices not in S[0] and triangle_vertices not in S[1] and triangle_vertices not in S[2]:
            S[3].add(triangle_vertices)
            
    return S
    
# =============================================================================
# function extract_triangle_vertices(triangle): list -> list
#
# extract_triangle_vertices takes the first three objects in the list triangle, 
#   fixing the second and sorting the other two. This is designed to get the appropriate
#   list of vertices from examples.triangle_type() to be used in the argument of
#   dtrl.double_triangle_reduction(). The sorting is done as the triangles
#   [0,1,2] and [2,1,0] are considered the same, as only the middle value is of
#   positional importance.
# =============================================================================
    
def extract_triangle_vertices(triangle):
    triangle_vertices=sorted([triangle[0],triangle[2]])
    triangle_vertices.insert(1,triangle[1])
    triangle_vertices=tuple(triangle_vertices)
    return triangle_vertices


# =============================================================================
# function triangle_type(Type): integer -> Graph
# This function takes an integer 0<n<5 and outputs a "triangle" of the corresponding
#   type. See Figure 4.10 (Page 38-9) of thesis. The triangle to be expanded is
# [0,1,2] with 1 the special vertex.
# =============================================================================

def triangle_type(Type):
    
    if Type==1:
        return Graph([[0,1],[0,2],[1,2],[0,3],[2,3],[1,4],[1,5],[4,5]])
    elif Type==2:
        return Graph([[0,1],[0,2],[1,2],[0,3],[2,3]])
    elif Type==3:
        return Graph([[0,1],[0,2],[1,2],[1,3],[1,4],[3,4]])
    elif Type==4:
        return Graph([[0,1],[0,2],[1,2]])
    else:
        raise ValueError('Argument of triangle_type(Type) must be an integer 0<n<5.')
        
        
# =============================================================================
# 
# =============================================================================