#######################################################################
# Executing this file produces the objects required to execute
# K5dsearch(start,target,Gseq,SVseq,parents,expanded). Use start=1.
#
# Note that this erases any previously stored output of K5dsearch from
#  memory.
#

version=0
Gseq=[[] for i in range(0,5)]
SVseq=dict()
expanded=dict()
lst1=[[] for i in range(0,11)]
Gseq.append(lst1)
Gseq[5][10].append([[graphs.CompleteGraph(5)]])
SVseq[tuple([5,10,0,0,0])]=tuple([tuple([tuple([10]),tuple([])])])
expanded[tuple([5,10,0,0,0])]=0
parents=dict()