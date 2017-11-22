#######################################################################
# This function converts a standard vector representation to a graph.
# If using a chord vector, use 
#   convertsvtograph(chainlist,cl=chordvector).
# If using a chord length vector clv, use 
#   convertsvtograph(chainlist,cl=clv).


def convertsvtograph(chainlist,cl=0,cll=0):
    newchainlist=list(chainlist)
    
    if len(chainlist)==1:
        return createZ(chainlist[0]) 
        
    #This step divides the lone vertices, so that it can be used as
    # input for the skeleton() function. We convert, e.g., [1,2,0,-3]
    # to [1,2,0,-1,-1,-1].
    l=newchainlist[-1]
    if l<0:
        newchainlist[-1]=-1
        l+=1
        while l<0:
            newchainlist.append(-1)
            l+=1
    
    #skeleton(chainlist) creates a skeleton that has the corresponding
    # chainlist. There are no chord edges yet, and those will be added
    # later.
    G=skeleton(newchainlist)[0]
    chainvertexlist=listchains(G)[1]
    L=deepcopy(G.vertices())
    #G.allow_multiple_edges(1)
    
    #The following piece of code calculates the position of each vertex
    # based on the definition of the standard vector, and assigns
    # chords to each position.     
    positionindex=0
    if cl:
        chordindex=0
        chords=dict()
    position=dict()
    valency=dict()
    newchainvertexlist=[]
    for chain in iter(chainvertexlist):
        for zigzg in iter(chain):
            zigzag=sorted(zigzg)
            for i in range(0,len(zigzag)):
                try:
                    L.remove(zigzag[i])
                except:
                    continue
                    
                if G.degree(zigzag[i])==2:
                    position[positionindex]=[zigzag[i]]
                    if cl:
                        chords[positionindex,0]=[
                            chordlist[chordindex],chordlist[chordindex+1]]
                        chordindex+=2
                    valency[positionindex,0]=2
                    positionindex+=1
                elif G.degree(zigzag[i])==3:
                    if len(zigzag)==4:
                        if positionindex not in position:
                            position[positionindex]=[zigzag[i]]
                            valency[positionindex,0]=1
                            if cl:
                                chords[positionindex,0]=[
                                    chordlist[chordindex]]
                                chordindex+=1
                        else:
                            position[positionindex].append(zigzag[i])
                            valency[positionindex,1]=1
                            if cl:
                                chords[positionindex,1]=[
                                    chordlist[chordindex]]
                                chordindex+=1
                            positionindex+=1
                    else:
                        position[positionindex]=[zigzag[i]]
                        valency[positionindex,0]=1
                        if cl:
                            chords[positionindex,0]=[
                                chordlist[chordindex]]
                            chordindex+=1
                        positionindex+=1
       
    #This piece of code addes the lone vertices to the position and chord
    # dictionaries.
    if len(L)>0:
        vertex=L[0]
        l=-len(L)
        while l<0:
            position[positionindex]=[vertex]
            valency[positionindex,0]=4
            if cl:
                chords[positionindex,0]=[
                    chordlist[chordindex+i] for i in range(0,4)]
                chordindex+=4
            positionindex+=1
            vertex+=1
            l+=1
            
    #This piece of code calculates the condensed chordlengthlist.
    if cl:
        fpos,lpos=dict(),dict()
        chordlengthlist=[]
    if cl:
        for pos in range(0,positionindex):
            for subpos in range(0,len(position[pos])):
                for chord in iter(chords[pos,subpos]):
                    if chord not in fpos:
                        fpos[chord]=pos
                    else:
                        lpos[chord]=pos
                    
    #print(chords)
    #print(fpos)
    #print(lpos)
    
    if cl:
        chordlengthlist=[lpos[i]-fpos[i] for i in range(
            1,len(chordlist)/2+1)]                

    #This piece of code adds the remaining edges to the skeleton graph.
    H=deepcopy(G)
    chordindex=1
    posindex=0
    if not cl:
        chordlengthlist=deepcopy(cll)
    #print(valency)
    #print(chainvertexlist)
    #print(position)
    #print(chordlengthlist)
    
    while chordindex<len(chordlengthlist)+1:
        nextpos=1
        while nextpos:
            for i in range(0,len(position[posindex])):
                if valency[posindex,i]>0:
                    fv=position[posindex][i]
                    valency[posindex,i]-=1
                    nextpos=0
                    break
            if nextpos:
                posindex+=1
        lpos=posindex+chordlengthlist[chordindex-1]
        
        nextpos=1
        while nextpos:
            for i in range(0,len(position[lpos])):
                if valency[lpos,i]>0:
                    lv=position[lpos][i]
                    valency[lpos,i]-=1
                    nextpos=0
                    break   
            if nextpos:
                lpos+=1
        H.add_edge(fv,lv)
        chordindex+=1

    return H
            
                        
#######################################################################
#This function creates the graph of Zn, with n as input.
#

def createZ(n):
    G=Graph()
    G.add_vertices([i for i in range(0,n+2)])
    G.add_edges([i,mod(i+1,n+2)] for i in range(0,n+2))
    G.add_edges([i,mod(i+2,n+2)] for i in range(0,n+2))
    return G


#######################################################################

def pdplot(G,returnlatex=0,filename='fig',graphicsize=(8,8),
           vertexlabels=1):
    from sage.graphs.graph_latex import check_tkz_graph
    K,color,colorlist=pdrelabel(G,outputcolor=1)
    
    if returnlatex:
        check_tkz_graph()
        K.set_pos(K.layout_circular(radius=3))
        plt=plot(K,layout='circular',vertex_colors=color,vertex_size=400)
        K.set_latex_option(tkz_style,'Normal')
        K.set_latex_options(vertex_label_colors=colorlist,
                            graphic_size=graphicsize)
        if not vertexlabels:
            K.set_latex_option(vertex_labels,0)
        opts=K.latex_options()
        with open(filename+".tex", "wb") as f:
            f.write(opts.tkz_picture())
        return plt
        
    return plot(K,layout='circular',vertex_colors=color)
 
    
#######################################################################    
    
    
    
    
    
    
    