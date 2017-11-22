####################################################################### 

def dtriancestor(G):
    A=copy(G)
    notri=0
    while not notri:
        dt=finddtri(A)
        if dt!=None:
            dtrired(A,dt[0],dt[1],dt[2],dt[3])
        else:
            notri=1
    return A

    
#######################################################################

def dtri(G,v1,v2,v3,c):
    G.delete_edge(v1,v2)
    vn=max(G.vertices())+1
    G.add_edges(((v1,vn),(v2,vn),(v3,vn)))
    S=setminus(G.neighbors(v3),(v1,v2,vn))
    if len(S)==1:
        c=0
    G.delete_edge(S[c],v3)
    G.add_edge(S[c],vn)
    return


#######################################################################

def dtrired(G,v1,v2,v3,v4):
    G.delete_edges([(v1,v4),(v2,v4),(v3,v4)])
    v=G.neighbors(v4)[0]
    G.add_edges([(v1,v3),(v,v2)])
    G.delete_vertex(v4)
    return


####################################################################### 

def finddtri(G):
    A=copy(G)
    A1=A.vertex_iterator()
    for i in A1:
        A2=A.neighbor_iterator(i)
        for j in A2:
            A.delete_edge(i,j)
            A3=A.neighbor_iterator(j)
            for k in A3:
                if not A.has_edge(i,k):
                    A.delete_edge(j,k)
                    A4=A.neighbor_iterator(k)
                    for l in A4:
                        if A.has_edge(i,l) and A.has_edge(
                            j,l) and A.has_edge(k,l):
                            A.delete_edges([(i,l),(j,l),(k,l)])
                            m=A.neighbors(l)[0]
                            if not A.has_edge(j,m):
                                return [i,j,k,l]
                            A.add_edges([(i,l),(j,l),(k,l)])
                    A.add_edge(j,k)
            A.add_edge(i,j)
    return None


#######################################################################

def isk5dsc(G):
    A=copy(G)
    n=A.order()
    A.allow_multiple_edges(1)
    while n>5:
        dt=finddtri(A)
        if dt!=None:
            dtrired(A,dt[0],dt[1],dt[2],dt[3])
            n-=1
            print(n)
        else:
            print('notri')
            return 0
    print('iso')
    return A.is_isomorphic(graphs.CompleteGraph(5))

#######################################################################