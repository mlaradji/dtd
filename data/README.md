Note that this data, although (hopefully) valid, does not play well with the new functions. A converter for the data will probably be uploaded soon.

 - descendants.file
 
 - Object Type: list
 
 - Importing using the pickle module:
 
    with open("descendants.file", "rb") as f:
        family = pickle.load(f)
    
    return
    
 - family[order][level][chno][zgno][index][i]
 
 order: number of vertices
 
 level: (number of vertices) - (number of triangles)    (Exception: Although K5 and K5's child have level<0, their level in the list is 0.)
 
 chno: number of open chains of zigzags
 
 zgno: number of zigzags
 
 index: distinguishes different graphs with the same order, level, chno and zgno
 
 i: i=0,1,2
    i=0: Graph object
    i=1: vector form of the graph
    i=2: "expanded" vector, which contains information about the triangle types that have been exhausted in the descendant search

