#######################################################################
# Input: L is a list of nonnegative integers.
# Output: descendants - list of descendants with L as their chain vector.
#         illegals - list of pseudo-descendants with chain vector L.
# Example input: L=[3,3,3], L=[3,3,0] or L=[3,0,3,0,-1].
#
# Note that if there are several lone vertices, then each one is to be
#   represented as -1 in L.

def listgraphs3(L):
    S,V1,V2,V4=skeleton(L)
    Lz=listzigzags(S)
    noftri=0
    for i in iter(L):
        if i>0:
            noftri+=i
    descendants=[]
    illegals=[]
    K5=graphs.CompleteGraph(5)
    possibleneighborsr=dict()
    remainingdegree=dict()
    Vs=set(union(set(V1),union(set(V2),set(V4))))
    for i in iter(V1):
        possibleneighborsr[i]=Vs.difference(set(
            returnzigzagcontainingvertex(Lz,i)))
        possibleneighborsr[i].discard(i)
        remainingdegree[i]=1
    for i in iter(V2):
        possibleneighborsr[i]=Vs.difference(set(
            returnzigzagcontainingvertex(Lz,i)))
        possibleneighborsr[i].discard(i)
        remainingdegree[i]=2
    for i in iter(V4):
        possibleneighborsr[i]=copy(Vs)
        possibleneighborsr[i].discard(i)
        remainingdegree[i]=4
    possibleneighbors=copy(possibleneighborsr)
    v=Vs.pop()
    Vs.add(v)
    possibleedgeslist=deque([deque([(v,i) for i in iter(
        possibleneighbors[v])])])
    edgeslist=deque()
    nofmissingedges=(len(V1)+2*len(V2)+4*len(V4))/2
    print(nofmissingedges)
    length=1
    while length>0:
        if len(possibleedgeslist[-1])>0:
            edge=possibleedgeslist[-1].pop()
            edgeslist.append(edge)
            if len(edgeslist)<nofmissingedges:
                u=edge[0]
                v=edge[1]
                possibleneighbors[u].discard(v)
                possibleneighbors[v].discard(u)
                remainingdegree[u]-=1
                remainingdegree[v]-=1
                if remainingdegree[u]==0:
                    Vs.discard(u)
                    for i in iter(Vs):
                        possibleneighbors[i].discard(u)
                if remainingdegree[v]==0:
                    Vs.discard(v)
                    for i in iter(Vs):
                        possibleneighbors[i].discard(v)
                u=Vs.pop()
                Vs.add(u)
                possibleedgeslist.append(
                    deque([(u,i) for i in iter(possibleneighbors[u])]))
                length+=1
            else:
                K=copy(S)
                K.add_edges(edgeslist)
                edgeslist.pop()
                if K.is_connected() and K.is_regular(
                ) and K.triangles_count()==noftri:
                    if dtriancestor(K).order()==5:
                        iso=0
                        for D in iter(descendants):
                            if K.is_isomorphic(D):
                                iso=1
                                break
                        if not iso:
                            descendants.append(K)
                    else:
                        iso=0
                        for I in iter(illegals):
                            if K.is_isomorphic(I):
                                iso=1
                                break
                        if not iso:
                            illegals.append(K)
        else:
            possibleedgeslist.pop()
            length-=1
            if len(edgeslist)>0:
                edge=edgeslist.pop()
                u=edge[0]
                v=edge[1]
                possibleneighbors[u].add(v)
                possibleneighbors[v].add(u)
                remainingdegree[u]+=1
                remainingdegree[v]+=1
                for i in iter(Vs):
                    Cu=u in possibleneighborsr[i]
                    Cv=v in possibleneighborsr[i]
                    if not conts(edgeslist,(i,u)) and not S.has_edge(i,u):
                        possibleneighbors[i].add(u)
                    if not conts(edgeslist,(i,v)) and not S.has_edge(i,v):
                        possibleneighbors[i].add(v)
                Vs.add(u)
                Vs.add(v)
    return descendants, illegals


####################################################################### 

def skeleton(L):
    G=graphs.CompleteGraph(0)
    ind=0
    V1=[]
    V2=[]
    V4=[]
    for i in range(0,len(L)):
        if L[i]>0:
            zigzag(G,[j+ind for j in range(0,L[i]+2)])
            if L[i-1]<1:
                #if L[i-1]==-1:
                #    if i>=1:
                #        G.add_edge(ind-1,ind)
                #    V1.append(ind)
                #else:
                V2.append(ind)
            if L[i]>1:
                V1.append(ind+1)
                V1.append(ind+L[i])
            else:
                V2.append(ind+1)
            l=L[mod(i+1,len(L))]        
            if l>0:                
                ind+=L[i]+1
            elif l==0:
                V2.append(ind+L[i]+1)
                ind+=L[i]+2
            else:
                V1.append(ind+L[i]+1)
                ind+=L[i]+2
        elif L[i]==-1:
            G.add_vertex(ind)
            V4.append(ind)
            #if i>=1:
            #    G.add_edge(ind,ind-1)
            ind+=1
    if L[-1]>0 and L[0]>0:
        G.merge_vertices((0,ind))
    #elif L[0]==-1 or L[-1]==-1:
    #    G.add_edge(ind-1,0)
    return G,V1,V2,V4


####################################################################### 

def returnzigzagcontainingvertex(L,v):
    for l in L:
        if conts(l,v):
            return l
    return []


####################################################################### 