#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  10 15:53:21 2018

@author: Mohamed Laradji
"""

# =============================================================================
# Import statements 
# =============================================================================

# imports from built-ins

import copy
import collections
#import functools32 # Replace with functools when the switch to Python 3 is completed.

# imports from sage
from sage.graphs.graph import Graph
from sage.graphs.graph_generators import graphs

# imports from thirdparty
"""
try:
    from boltons import setutils  # Note that this requires to be installed.

except ImportError:
    from thirdparty.boltons import setutils
"""

# imports from common
#import common.graphs as cg
#import common.functions as cf

from common.functions import classproperty
from common.exceptions import InvalidHash, NoneReturned
#from common.exceptions import NotSubgraph, Underdefined
#from common.exceptions import UnsupportedOption

# object imports

#from search.Family import Family

# =============================================================================
# Class definitions 
# =============================================================================
    

class eGraph(Graph):
    '''
    This is an extension of the SageMath Graph class. This aims to contain functions that are not specific to $K_5$-descendants.
    '''
    
    # extra_attributes are attributes that need to be copied in addition to the Graph object, for a full copy.
    @classproperty
    def extra_attributes(cls):
        return {'counts': dict(), 'hashes': dict(), 'count_functions': dict()}
    
    def __init__(self, data=None, use_preset_count_functions=True, **kwargs): #immutable = True
        '''
        Can be initialized the same way as a sage Graph object.
        '''
        
        super(eGraph, self).__init__(data, **kwargs)
        
        # The self.counts dict contains precalculated information about Graph, and self.hashes will contain the hashes of the graph when those values were calculated. A value will be recalculated if current hash is different from when the value was calculated.
        self.counts = dict()
        self.hashes = dict()
        
        # self.count_functions is a count_name to function dictionary.
        self.count_functions = dict()
        
        if use_preset_count_functions:
            self.count_functions.update({
                'order': lambda G: G.order(),
                'triangles_count': triangles_count,
                'level': lambda G: G.order()-G.triangles_count(),
                'chromatic_number': lambda G: G.chromatic_number(),
                'connectivity': lambda G: G.connectivity(),
            })
                
        #if immutable: self = self.immutable_copy()
        
# =============================================================================

    def immutable_copy(self):
        '''
        Returns an immutable copy of self.
        '''
                                
        return self.ecopy(immutable = True)
    
# =============================================================================    

    def ecopy(self, immutable = False):
        '''
        Returns a copy of self. This is different from self.copy in that self.copy only copies the underlying SageMath Graph object, while self.ecopy also copies the extra_attributes. See self.extra_attributes for a list.
        '''
        
        return eGraph_copy(self, graph_class = self.__class__, immutable = immutable)
        

# =============================================================================  

    def hash(self):
        '''
        Returns the hash of an immutable copy of self.
        '''
        
        return hash(self.immutable_copy())

    
# =============================================================================
#   Counts
# =============================================================================

#         class graphproperty(dict):
#             '''
#             Adds caching.
#             '''

#             def __init__(self, func):
#                 self.func = func

#             def __call__(self, *args):
#                 return self[args]

#             def __missing__(self, key):
#                 result = self[key] = self.func(*key)
#                 return result

#     # =============================================================================
        
    def set_count(self, count_name, count_value = None, count_function = None):
        '''
        Adds or changes self.counts[count_name], count_name expected to be a string, and adds count_name to self.hashes.
        '''
        
        current_hash = self.hash()
        
        self.hashes[count_name] = current_hash
        
        if count_value is None and count_name in self.counts: 
            pass
        
        else:
            self.counts[count_name] = count_value 
        
        if count_function is None: pass
        else: self.count_functions[count_name] = count_function
        
        return 
    
# =============================================================================    
    
    def check_count(self, count_name):
        '''
        This checks if count_name is valid.
        '''
        
        current_hash = self.hash()
        
        if not count_name in self.counts:
            raise IndexError('count_name '+str(count_name)+' has not been calculated yet.')
            
        elif self.counts[count_name] is None:
            raise NoneReturned('count_name ' + str(count_name) + ' has not been calculated yet.')
        
        if current_hash != self.hashes[count_name]:
            raise InvalidHash('The count has not been verified for the current version of the graph.')
    
# =============================================================================    
    
    def count(self, count_name, count_function = None):
        '''
        Gets the count of count_name. Raises an IndexError exception if count_name has not been calculated, and an InvalidHash if count was calculated for an older version of the graph.
        '''
        
        try:
            self.check_count(count_name)
            return self.counts[count_name]
                             
        except (InvalidHash, IndexError, NoneReturned) as exc:
            pass
        
        if count_function is None: 
            try:
                count_function = self.count_functions[count_name]
            except KeyError:
                count_function = lambda G: getattr(G, count_name)() # This is a fallback mechanism.
            
        self.set_count(count_name, count_value = count_function(self), count_function = count_function) # Will be reset after every calculation. Desired?
        return self.counts[count_name]

# =============================================================================

    def list_counts(self, count_names = list()):
        '''
        This calculates the counts in count_names, returning it as a list of values. Useful for checking condition satisfaction or for sorting purposes. Input is expected to be ordered; for instance, a list, an IndexedSet or an OrderedDict.
        
        Example:
            G = graphs.CompleteGraph(5)
            G.counts(['order','triangles_count'])
            >> OrderedDict([('order', 5), ('triangles_count', 10)])
        '''
        
        counts = collections.OrderedDict()
        
        for count_name in count_names:
            counts[count_name] = self.count(count_name)
            
        return counts
    
# =============================================================================

    
    def triangles_count(self):
        '''
        Returns the number of triangles in self. This differs from Graph.triangles_count() in that it also works for multigraphs.
        '''
        
        count_function = triangles_count
        
        return self.count('triangles_count', count_function)
    
# =============================================================================        
    
    def level(self):
        '''
        Returns order-triangles_count.
        '''
        
        count_function = lambda G: G.order()-G.triangles_count()
        
        return self.count('level', count_function)
    
# ============================================================================= 

    def satisfies(self, conditions = dict()):
        '''
        Returns True if the graph satisfies the conditions, and False otherwise.

        Options:
            conditions -    dict -  A count_name to count_value dict. Eg, conditions = {'order': 3, 'triangles_count': 4}. An iterable object can also be used for count_value. Eg, conditions = {'order': [3,5]} 
        '''

        for count_name in conditions:
            # If count_value is iterable, iterate over those values.
            try:
                satisfied = False
                for count_value in conditions[count_name]:
                    if self.count(count_name) == count_value:
                        satisfied = True
                        break
                        
                if not satisfied: return False
                
            except TypeError:
                if not self.count(count_name) == conditions[count_name]: return False
                
        return True
    

# =============================================================================
#   Graph operations
# =============================================================================
    
    def identify_vertices(self,v1,v2):
        '''
        This identifies v2 with v1, and for every vertex u adjacent to v2, the edge (u,v1) is added. 
        '''

        
        for edge in self.edge_iterator([v2]):  # self.edge_iterator(vertices) seems to require that vertices is a list, even if it is a single vertex.
            
            if edge[0]==v2 and edge[1]==v2: self.add_edge(v1,v1)
            elif edge[0]==v2: self.add_edge(v1, edge[1])
            elif edge[1]==v2: self.add_edge(v1, edge[0])
            
            self.delete_edge(edge)
        self.delete_vertex(v2)
        
# =============================================================================

    def subdivide_edge(self, edge, divisions = 1):
        '''
        This attempts to have serve the same function as Graph.subdivide_edge().
        
        Returns the new vertices.
        '''
        
        self.delete_edge(edge)
        
        new_vertices = [self.add_vertex() for i in range(0,divisions)]
        
        new_path = collections.deque([edge[0]])
        new_path.extend(new_vertices)
        new_path.append(edge[1])
        
        vertex1 = new_path.pop()
        
        while True:
            try:
                vertex2 = new_path.pop()
                
                self.add_edge(vertex1, vertex2)
                
                vertex1 = vertex2
            
            except IndexError:
                break
        
        return new_vertices

# =============================================================================

    def symmetric_difference(self, graph):
        '''
        Returns a new graph that is the symmetric difference of self and graph, defined to be the graph that contains the edges that are in exactly one of self and graph.
        '''
        
        Edges1=self.edges()
        Edges2=graph.edges()
        
        symmetric_difference=eGraph(list(set(Edges1).symmetric_difference(Edges2)))
        
        return symmetric_difference
        
                
# ============================================================================= 

    def crossing_into_vertex(self, e1, e2):
        '''
        Subdivides e1, e2 and identifies the resultant degree 2 vertices. Returns the new vertex that was created.
        '''
    
        
        new_vertices = []
        new_vertices.extend(self.subdivide_edge(e1,1))
        new_vertices.extend(self.subdivide_edge(e2,1))
        
        
        if len(new_vertices)==2:
        # All is good.

            self.identify_vertices(new_vertices[0], new_vertices[1]) 
            # new_vertices[0] and new_vertices[1] are identified to be new_vertices[0].
    
        else:
            raise ValueError('new_vertices is expected to be of length 2. Received '+str(new_vertices)+' instead.')
            
        
        return new_vertices[0]

# ============================================================================= 


# =============================================================================
# Graph isomorphism
# =============================================================================
    
    def has_isomorphic_subgraph(self, graph):
        '''
        Returns True if self has graph as an isomorphic subgraph, and False otherwise.
        '''
        
        subgraph=self.subgraph_search(graph)
        
        if subgraph is None:
            return False
        
        else:
            return True

    
# =============================================================================
#   Standalone functions
# =============================================================================


def eGraph_copy(graph, graph_class = eGraph, immutable = False):
    '''
    Returns an eGraph copy of graph.
    
    Options:
        graph_class -   class -     The desired class of the new graph.  
        immutable -     bool -      Whether to return an immutable eGraph copy.
    '''
    
    # Convert graph into the specified class, and make it immutable if specified.
    G = graph_class(graph).copy(immutable = immutable) 
    
    for attr in G.extra_attributes:       
        try:
            setattr(G, attr, getattr(graph, attr))
        
        except AttributeError:
            setattr(G, attr, G.extra_attributes[attr])
    
    return G

# =============================================================================

def triangles_count(G): 
    '''
    This is a triangles_count that works for graphs with multiple edges, which relies on the Matrix Tree Theorem corollary that "trace(G.adjacency_matrix()**3/6)=triangles count". Note that it is quite slow.
    '''
    
    try:
        return super(eGraph, G).triangles_count()
    
    except ValueError:
        return (G.adjacency_matrix()**3/6).trace()
    
    
# =============================================================================
#     
#   Exceptions
#
# ============================================================================= 


# =============================================================================  


# =============================================================================
#   Deprecated
# =============================================================================

    
# =============================================================================  