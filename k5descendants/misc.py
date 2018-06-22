# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 17:11:23 2018

@author: mohamed
"""

#==============================================================================
# This library contains functions that do not really fit in any other
#	categories. Functions here might later become their own library or 
#	be assimilated to another library.
#==============================================================================


#==============================================================================
# 
#==============================================================================

def dodgson_polynomial(G,I=[],J=[],K=[]):
    # Karen's book
    if not len(I)==len(J):
        raise ValueError('We must have that |I|=|J|.')
            
    H=next(G.orientations()) # H is an arbitrary orientation of G.
    
    size=H.size()
    order=H.order()
    
    t = list(var('t%d' % i) for i in range(size)) 
    # The variables t0,t1,... are the ones used in the output polynomial.
    #R.<x,y,z> = QQ #The ring of integers is used. 

    gamma=vector([t[i] for i in range(size)])
    Gamma=diagonal_matrix(gamma)
    E=H.incidence_matrix().delete_rows([0])
    Et=E.transpose()
    Z=matrix.zero(order-1)

    
    Psi_matrix=block_matrix([[Gamma,Et],[-E,Z]])
    Psi_matrix=Psi_matrix.delete_rows(I)
    Psi_matrix=Psi_matrix.delete_columns(J)
    Psi=Psi_matrix.determinant()
    
    Psi=Psi.subs({t[k]:0 for k in iter(K)})
        
    return Psi
    
def five_invariant(G,i,j,k,l,m):
    # Karen's book
    f_1=dodgson_polynomial(G,[i,j],[k,l],[m])
    f_2=dodgson_polynomial(G,[i,k,m],[j,l,m])
    f_3=dodgson_polynomial(G,[i,k],[j,l],[m])
    f_4=dodgson_polynomial(G,[i,j,m],[k,l,m])
    
    return f_1*f_2-f_3*f_4

def c2_invariant(G,p,decomplete=True):    
    if decomplete:
        A=double_triangle_ancestor(G)
        A.delete_vertex(A.random_vertex())
        n=A.size()
    else:
        raise ValueError('Calculation of the ancestor has not yet been implemented for decompleted or non-4-regular graphs.')

    inv5=five_invariant(A,0,1,2,3,4)	
    count=0
    sol=[]
    for element in itertools.product(range(p),repeat=n-5):
        result=inv5.subs({t[i+5]:element[i] for i in range(n-5)})
        #print(int(result))
        if int(result)%p==0:
            sol.append(element)
            count+=1
    return (-1)**5*count%p
    #return (count+p^2)/p^3