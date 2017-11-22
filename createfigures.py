#######################################################################

#filename1='k5d50300'
#filename2='nonk5d50300'
#graphicsize=(6,6)
#G=Gseq[13][8][2][1][0]
#SV=standardvector(G)
#H=convertsvtograph(SV[0],cll=SV[1])
#H.delete_edges([[5,12],[6,7]])
#H.add_edges([[6,12],[5,7]])
#pdplot(G,1,filename1,graphicsize)
#pdplot(H,1,filename2,graphicsize)


#######################################################################
graphicsize=(4,4)
with open("figurefilenames.tex", "wb") as f:
    for n in range(0,len(Gseq)):
        for t in range(0,len(Gseq[n])):
            for c in range(0,len(Gseq[n][t])):
                for l in range(0,len(Gseq[n][t][c])):
                    for i in range(0,len(Gseq[n][t][c][l])):
                        G=deepcopy(Gseq[n][t][c][l][i])
                        filename='k5dlistn'+str(n)+'t'+str(t)+'c'+str(
                            c)+'l'+str(l)
                        pdplot(G,1,filename,graphicsize,vertexlabels=0)
                        f.write('\input{'+filename+'.tex}\n')     
                               
#######################################################################