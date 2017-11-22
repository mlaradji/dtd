#######################################################################
# Input: start - The order at which to start the search. Note that
#                Gseq must contain at least one graph of order start-1.
#                If initializevectorsearch.py is executed, use start=1.
#        target - The order at which to stop.
#        Gseq - List of K5 descendants. Gseq[order][tri] is a list
#               containing graphs with order vertices and tri triangles.
#        SVseq - dictionary with keys (order, triangle count, index).
#                SVseq[(order, tri, index)] gives the standard
#                vector of Gseq[order][tri][index].
#        parents - dictionary with keys (order, triangle count, index).
#                  parents[(order, tri, index)] gives the standard
#                  representation of the parents of
#                  Gseq[order][tri][index].
#        expanded - dictionary with keys (order, triangle count, index).
#                   expanded[(order, tri, index)]=1 if all the
#                   descendants of Gseq[order][tri][index] have been
#                   found, 0 otherwise.
#
# Output: Gseq, SVseq, parents, expanded
#
# Note 1: Gseq and SVseq are only saved in memory, and not to disk. To
#  save to disk, use the command execfile('k5dsearch_save.py'). To load
#  from disk, use the command execfile('k5dsearch_load.py').
#
# Note 2: The parents dictionary is currently disabled due to bugs.
#

def K5dsearch(start,target,Gseq,SVseq,parents,expanded):

    start_time = time.time()
    for order in range(start,target+1):
    
        while len(Gseq)<order+1:
            Gseq.append([[]])
        
        int_time, nc_time=time.time(),time.time()
    
        for tricount in range(0,len(Gseq[order-1])):
            for chaincount in range(0,len(Gseq[order-1][tricount])):
                for lonecount in range(0,len(
                    Gseq[order-1][tricount][chaincount])):
                    for index in range(0,len(
                        Gseq[order-1][tricount][chaincount][lonecount])):
                        G=copy(Gseq[order-1][tricount][
                            chaincount][lonecount][index])
                        triset=set()
                        if not expanded[tuple([order-1,tricount,
                                               chaincount,
                                               lonecount,index])]:
                            trilist=listtriangles(G)
                            for i in range(0,3):
                                triset=triset.union(trilist[i])

                        for tri in triset:
                            candidate=copy(G)
                            dtri(candidate,tri[1],tri[2],tri[0],0)
                            candidate=pdrelabel(candidate)
                            candSV=tuple(standardvector(candidate))
                            candPDparam=PDparameters(candSV[0])
                            candtricount=candPDparam[0]
                            candchaincount=candPDparam[1]
                            candlonecount=candPDparam[3]
                            
                            while len(Gseq[order])<candtricount+1:
                                Gseq[order].append([])
                            while len(Gseq[order][
                                candtricount])<candchaincount+1:
                                Gseq[order][candtricount].append([])
                            while len(Gseq[order][candtricount][
                                candchaincount])<candlonecount+1:
                                Gseq[order][candtricount][
                                    candchaincount].append([])
                                
                            iso=0
                
                            for i in range(0,len(Gseq[order][
                                candtricount][candchaincount][
                                candlonecount])):
                                if candSV[0]==SVseq[tuple([
                                    order,candtricount,
                                    candchaincount,candlonecount,i])][0]:
                                    
                                #parents[
                                #    tuple([order,candtricount,i])].add(
                                #    tuple([order-1,tricount,index]))
                                    if candidate.is_isomorphic(Gseq[
                                        order][candtricount][
                                        candchaincount][candlonecount][i]):
                                        iso=1
                                        break
                
                            if not iso:
                                Gseq[order][candtricount][
                                    candchaincount][
                                    candlonecount].append(candidate)
                                tpl=tuple([order,candtricount,
                                           candchaincount,candlonecount,len(
                                               Gseq[order][candtricount][
                                                   candchaincount][
                                                   candlonecount])-1])
                                SVseq[tpl]=candSV
                                #parents[tpl]=set([tuple([
                                #    order-1,tricount,index])])
                                expanded[tpl]=0
                    
                        expanded[tuple([order-1,tricount,
                                        chaincount,lonecount,index])]=1
                               
        print(str(order)+'-'+str(time.time() - int_time))
    print("--- %s seconds ---" % (time.time() - start_time))
    

#######################################################################