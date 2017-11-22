#######################################################################
# Some set functions

def inter(A,B):
    C=[]
    for i in range(0,len(A)):
        for j in range(0,len(B)):
            if A[i]==B[j]:
                C.append(A[i])
    return C

def conts(A,a):
    cont=0
    for i in range(0,len(A)):
        if a==A[i]:
            cont=1
            break
    return cont

def setminus(A,B):
    C=[]
    for i in range(0,len(A)):
        if not conts(B,A[i]):
            C.append(A[i])
    return C


#######################################################################
#cyclicpermutations produces an iterable of a cyclic permutation of 
# length "length".

def cyclicpermutations(length):
    S=[i for i in range(0,length)]
    index=0
    while 1:
        yield S
        index+=1
        if index==length:
            raise StopIteration
        S=[S[mod(i+1,length)] for i in range(0,length)]
        
        
#######################################################################      

def sumvectors(v1,v2):
    return tuple([v1[i]+v2[i] for i in range(0,len(v1))])


#######################################################################

def modvector(vector,modulus):
    workingvector=list(vector)
    for i in range(len(vector)-1,0,-1):
        v=workingvector[i]
        m=modulus[i]
        quotient=int(v/m)
        remainder=v-m*quotient
        workingvector[i]=remainder
        workingvector[i-1]+=quotient
    workingvector[0]=mod(workingvector[0],modulus[0])
    return tuple(workingvector)


#######################################################################
        
def itertuples(moduluslist):
    unit=[0 for i in range(0,len(moduluslist)-1)]
    zerovector=copy(unit)
    zerovector.append(0)
    zerovector=tuple(zerovector)
    unit.append(1)
    unit=tuple(unit)
    tpl=zerovector
    while 1:
        yield tpl
        tpl=modvector(sumvectors(tpl,unit),moduluslist)
        if tpl==zerovector:
            raise StopIteration
            

#######################################################################           
            
def chainsignlist(lengthlist,symmetriclist):
    S=[itertuples([symmetriclist[i]+1 for j in range(
        0,lengthlist[i])]) for i in range(0,len(lengthlist))]
    CS=[S[i].next() for i in range(0,len(S))]
    index=0
    found=0
    while 1:
        yield CS
        while not found:
            try:
                CS[index]=S[index].next()
                found=1
            except StopIteration:
                S[index]=itertuples([symmetriclist[
                    index]+1 for j in range(
                    0,lengthlist[index])])
                CS[index]=S[index].next()
                index+=1
                if index==len(lengthlist):
                    raise StopIteration
        found=0
        index=0

        
#######################################################################
#chainpermutations takes a list of positive integers, and produces 
# as an output an iterable of a list of permutations of lengths as in 
# lengthlist.

def chainpermutations(lengthlist):
    P=[itertools.permutations(range(0,lengthlist[i])) for i in range(
        0,len(lengthlist))]
    CP=[P[i].next() for i in range(0,len(P))]
    index=0
    found=0
    while 1:
        yield CP
        while not found:
            try:
                CP[index]=P[index].next()
                found=1
            except StopIteration:
                P[index]=itertools.permutations(range(0,lengthlist[
                    index]))
                CP[index]=P[index].next()
                index+=1
                if index==len(lengthlist):
                    raise StopIteration
        found=0
        index=0


#######################################################################

def symmetricvector(v):
    return list(v)==list(reversed(v))


#######################################################################