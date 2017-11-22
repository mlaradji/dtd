#######################################################################

def standardvector(G):
    
    if iszigzag(G):
        return tuple([tuple([G.triangles_count()]),tuple()])
    
    K=pdrelabel(G)
    
    #This piece of code constructs an ordered list of edges that are not
    # in chains. These will be the "chords" in our graph.
    #
    
    chainlist,chainvertexlist=listchains(K)
    chainlist,chainvertexlist=orderchainlist(chainlist,chainvertexlist)
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
    
    position=positionsofvertices(H,chainvertexlist,lonevertices)
    #print(position)
    poc=dict() #positions of chords
    
    for i in range(0,len(E)):
        u,v=E[i][0],E[i][1]
        pos1 = next(key for key, value in position.items() if u in set(value))
        pos2 = next(key for key, value in position.items() if v in set(value))
        poc[i]=[pos1,pos2]
    
    chordlengthvector=[abs(poc[i][1]-poc[i][0]) for i in range(0,len(E))]
    chainv=chainvector(chainlist,len(lonevertices))
    
    return chainv,chordlengthvector


#######################################################################

def chainvector(chainlist,lvcount):
    cv=[]
    cond0=len(chainlist)==1 and lvcount==0
    
    for chain in iter(chainlist):                   
        for Z in iter(chain):
            cv.append(Z)
        if not cond0:
            cv.append(0)
    
    if lvcount>0:
        cv.append(-lvcount)
        
    return tuple(cv)


#######################################################################

def positionsofvertices(G,chainvertexlist,lvlist):
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

#######################################################################

def pdrelabel(G,outputcolor=0,colorlist=0):
    if iszigzag(G):
        return G
    
    chainlist,chainvertexlist=listchains(G)
    chainvertexlist,chainlist=orderchainlist(chainvertexlist,chainlist)
    
    #H=deepcopy(G)
    K=deepcopy(G)
    lv=K.vertices()
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


#######################################################################

def orderchainlist(chainlist,chainvertexlist):
    for i in range(0,len(chainlist)):
        C=chainvertexlist[i]
        c=chainlist[i]
        C,c=orderchain(C,c)
        c=list(c)
        chainvertexlist[i]=C
        c.append(-i)
        chainlist[i]=tuple(c)
        
    chainlist=mergesort(chainlist)
    newchainvertexlist=[]
    
    for i in range(0,len(chainlist)):
        identifier=-chainlist[i][-1]
        chainlist[i]=tuple(chainlist[i][0:-1])
        newchainvertexlist.append(chainvertexlist[identifier])
        
    return chainlist,newchainvertexlist

#######################################################################
# obtained from pythonandr.com/2015/07/05/the-merge-sort-python-code/
# Author: Anirudh Jay (pythonandr.com/author/anirudhjay/)

def merge(a,b):
    """ Function to merge two arrays """
    c = []
    while len(a) != 0 and len(b) != 0:
        if a[0] < b[0]:
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        c += b
    else:
        c += a
    return c

# Code for merge sort

def mergesort(x):
    """ Function to sort an array using merge sort algorithm """
    if len(x) == 0 or len(x) == 1:
        return x
    else:
        middle = len(x)/2
        a = mergesort(x[:middle])
        b = mergesort(x[middle:])
    return merge(a,b)
 
        
#######################################################################

def orderchain(C,c):
    maxC=C
    maxc=tuple(c)
    n=len(c)
    
    for P in cyclicpermutations(n):
        for i in range(0,2):
            if i:
                newc=tuple([c[P[n-1-i]] for i in range(0,n)])
            else:
                newc=tuple([c[P[i]] for i in range(0,n)])

            if newc>maxc:
                maxc=newc
                maxC=[C[P[i]] for i in range(0,n)]
            
    return maxC,maxc


#######################################################################

def chainsize(C,c):
    size=0
    for i in range(0,len(c)):
        size+=c[i]
    return size


#######################################################################