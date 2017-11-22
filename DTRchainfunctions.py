#######################################################################
#listchains(G) creates two lists from G, the first of which is a list
# of lists (chains) of zigzag lengths. The second list is a list of lists
# of lists of zigzag vertices.
# 
# Example output: [[3, 3]], [[[0, 6, 7, 4, 1], [1, 5, 8, 2, 3]]]
#

def listchains(G):
    A=copy(G)
    reversedir=0
    startnewchain=1
    chainlist=[]
    chainvertices=[]

    while A.triangles_count()>0:
        
        if startnewchain:
            Z=findzigzag(A,-1)
            A.delete_vertices(Z[1:-1])
            if A.subgraph(Z).is_regular(4):
                tri=len(Z)
            else:
                tri=len(Z)-2
            chainlist.append([tri])
            chainvertices.append([Z])
            startnewchain=0
            currfirstval=Z[0]
            currlastval=Z[-1]
        
        else:
            if reversedir:
                val=chainvertices[-1][0][0]
                Z=findzigzag(A,val)

                if not Z:
                    A.delete_vertex(val)
                    startnewchain=1
                    reversedir=0
                else:
                    if Z[0]==val:
                        Z.reverse()
                    tri=len(Z)-2
                    chainlist[-1].insert(0,tri)
                    chainvertices[-1].insert(0,Z)
                    A.delete_vertices(Z[1:-1])

            else:
                val=chainvertices[-1][-1][-1]
                Z=findzigzag(A,val)
                #print(val)
                #print(A.edges())

                if not Z:
                    A.delete_vertex(val)
                    reversedir=1
                else:
                    if Z[-1]==val:
                        Z.reverse()
                    tri=len(Z)-2
                    chainlist[-1].append(tri)
                    chainvertices[-1].append(Z)
                    A.delete_vertices(Z[1:-1])
        
    return chainlist, chainvertices


#######################################################################
#findtri returns a triangle in G if s is unspecified. If s>=0, it 
# returns a triangle containing s. If G containts no triangles,
# it returns 0.

def findtri(G,s=-1):
    A=copy(G)
    if s!=-1 and A.has_vertex(s):
        A1=iter([s])
    else:
        A1=A.vertex_iterator()
    for i in A1:
        for j in A.neighbor_iterator(i):
            A.delete_edge(i,j)
            for k in A.neighbor_iterator(j):
                if A.has_edge(i,k):
                    return [i,j,k]
            A.add_edge(i,j)
    return 0


#######################################################################
#findzigzag starts with a triangle and finds a maximal zigzag containing 
# that triangle. If G contains no triangles, it returns 0.
# If s is specified, it returns a zigzag containing the vertex s if it 
# exists, and 0 otherwise.

def findzigzag(G,s=-1):
    A=copy(G)
    if A.triangles_count()==0:
        return 0
    Z=findtri(A,s)
    if not Z:
        return 0
    
    L=[]
    for i in range(0,2):
        for j in range(i+1,3):
            L.append([Z[i],Z[j]])
            A.delete_edge([Z[i],Z[j]])
    k=0
    while len(L)>k:
        V=inter(A.neighbors(L[k][0]),A.neighbors(L[k][1]))
        if len(V)==0:
            k+=1
        else:
            v=V[0]
            Z.append(v)
            L.append([v,L[k][0]])
            L.append([v,L[k][1]])
            A.delete_edges([(v,L[k][0]),(v,L[k][1])])
            k+=1

    if len(Z)>3:
        H=G.subgraph(Z)
        for i in range(0,len(Z)):
            if H.degree(Z[i])==2:
                Zo=[Z[i]]
                break
        N=H.neighbors(Zo[0])
        for i in range(0,len(N)):
            if H.degree(N[i])==3:
                Zo.append(N[i])
                break
        H.delete_edge(Zo)
        
        i=0
        while H.size()>0:
            S=inter(H.neighbors(Zo[i]),H.neighbors(Zo[i+1]))
            Zo.append(S[0])
            H.delete_edges([(Zo[i],S[0]),(Zo[i+1],S[0])])
            i+=1
    elif len(Z)==3:
        Zo=Z
        if G.cluster_triangles(Z[1])==2:
            Zo=[Zo[0],Zo[2],Zo[1]]
            
        if s!=Z[0] and G.cluster_triangles(
            Z[0])==1 and G.cluster_triangles(Z[1])==2:
            Zo=[Zo[1],Zo[0],Zo[2]]
    
    return Zo


#######################################################################

def listtriangles(G):
    A=copy(G)
    S0=set()
    S1=set()
    S2=set()
    for v1 in A.vertex_iterator():
        for v2 in A.neighbor_iterator(v1):
            S=set([v1,v2])
            for v3 in A.neighbor_iterator(v2):
                if v3>v2 and v3 not in S and A.has_edge(v1,v3):
                    S=set([v1,v2,v3])
                    S0.add((v1,v2,v3))
                    for v4 in A.neighbor_iterator(v2):
                        if v4 not in S and A.has_edge(v2,v4) and A.has_edge(
                            v3,v4):
                            S1.add((v1,v2,v3))
                    for v4 in A.neighbor_iterator(v1):
                        if v4 not in S:
                            S=set([v1,v2,v3,v4])
                            for v5 in A.neighbor_iterator(v4):
                                if v5>v4 and v5 not in S and A.has_edge(
                                    v1,v5):
                                    S2.add((v1,v2,v3))
    S12=S1.union(S2)
    T2=S1.intersection(S2)
    T1=S12.difference(T2)
    T0=S0.difference(S12)
    return T0,T1,T2


#######################################################################

def listuniquetriangles(G):
    chainlist,chvertexlist=listchains(G)
    trilist=listtriangles(G)
    trilist0=trilist[0]
    newT0=set()
    found=dict()
    for i in range(0,len(chainlist)):
        for j in range(0,len(chainlist[i])):
            if chainlist[i][j]>=1:
                tpl=iter([i,j])
                for k in iter(chvertexlist[i][j][1:-1]):
                    toremove=set()
                    for tri in iter(trilist0):
                        if tri[0]==k:
                            if tpl not in found:
                                newT0.add(tri)
                                found[tpl]=1
                            toremove.add(tri)
                        
                    trilist0=trilist0.difference(toremove)
    return newT0,trilist[1],trilist[2]