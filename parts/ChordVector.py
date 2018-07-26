#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 17:13:18 2018

@author: Mohamed Laradji
"""


from common import exceptions

# =============================================================================
# class ChordVector
#
#   This class aims to contain various useful tools to deal with chord vectors,
#       especially converting between different forms.
#
#   The default list in a ChordVector is the position_edges, which denotes which
#       positions are adjacent to each other.
# =============================================================================

class ChordVector:
    
    type = 'ChordVector'
    
    def __init__(self, chord_vector=None, chord_edges=None, position_edges=None, parent_object=None, max_degree=4):
        
        #if chord_vector is None: chord_vector=tuple([])
        
        self.set_parent_object(parent_object)
        self.set_max_degree(max_degree)
        #self.set_chord_vector(chord_vector)
        
        if chord_vector is None:
        
            if chord_edges is not None:
                if position_edges is None:
                    
                    position_edges=self.chord_to_position_edges(chord_edges)
                    
                else:
                    raise Overdefined('At most one of chord_edges and position_edges must be defined.')
                    
                #chord_vector=self.make_chord_vector(position_edges=position_edges)
                #self.set_position_edges
                    
            
            #elif position_edges is not None:
                #chord_vector=self.make_chord_vector(chord_edges=chord_edges)
                
                
        elif chord_edges is not None or position_edges is not None:
            raise Overdefined('At most one of chord_vector, chord_edges, and position_edges must be defined.')
            
        else: position_edges=self.make_position_edges(chord_vector)
        
        self.set_position_edges(position_edges)
        
    
    def chord_to_position_edges(self, chord_edges=None):
        if chord_edges is None: return []
        
        position_edges=[]
        
        for chord_edge in iter(chord_edges):
            
            position_dict=self.position_dict(position_to_vertex=False)  # position_dict here is a vertex to position dict.
            
            position_edge=(position_dict[chord_edge[0]], position_dict[chord_edge[1]])
            
            position_edges.append(position_edge)
            
        return position_edges
    

    
    def set_position_edges(self, position_edges=None):
        if position_edges is None: position_edges=[]
        
        self.position_edges=position_edges
        return
    
    
    def positions(self, parent_object=None, with_labels=False):
        if parent_object is None: 
            if self.parent_object is None:
                raise MissingParentObject('positions requires a parent object. Either set the parent object using self.set_parent_object, or use the argument parent_object.')
                
            else:    
                parent_object=self.parent_object
                
        external_vertices=self.parent_object.external_vertices()
        
        if with_labels: return external_vertices
        else: return [i for i in range(0,len(external_vertices))]
        
    def no_of_positions(self):
        # This function counts the number of positions, based on the parent object.
        return len(self.positions())
    
    def make_position_edges(self, chord_vector=None, parent_object=None):
        
        # This function creates a list of edges based on the positions (rather
        #   than vertex labels). That is, (i,j) means position i is adjacent to 
        #   position j. Note that the if parent_object is not None, it will be 
        #   used instead of self.parent_object.
        #
        #   If make_positions=True, the output will be a list of two items,
        #       the position_edges and positions lists.
        
        if parent_object is None: 
            if self.parent_object is None:
                raise MissingParentObject('make_position_edges requires a parent object. Either set the parent object using self.set_parent_object, or use the argument parent_object.')
                
            else:    
                parent_object=self.parent_object
        
        if chord_vector is None: return []
        
        skeleton_degree=self.parent_object.skeleton_degree()
        
        external_vertices=self.parent_object.external_vertices()
        no_external_vertices=len(external_vertices)
        
        position_edges=[]
        
        chords=iter(chord_vector)       
         
        for vertex1 in range(0,no_external_vertices):

            remaining_degree=self.max_degree-skeleton_degree[vertex1]
            
            while remaining_degree>0:
            
                try:
                    vertex2=(vertex1+chords.next())%no_external_vertices
                    position_edges.append((vertex1, vertex2))
                    remaining_degree-=1
                    
                except StopIteration:
                    break
        
        return position_edges
    
    
    def chord_edges(self, parent_object=None):
        # This function creates a list of chord edges based on the external vertices
        #   and the supplied chord_vector or self.chord_vector
        
        
        if parent_object is None: 
            if self.parent_object is None:
                raise MissingParentObject('chord_edges requires a parent object. Either set the parent object using self.set_parent_object, or define the argument parent_object.')
                
            else:    
                parent_object=self.parent_object
        
        #if self.chord_vector is None: return []
        
        position_edges=self.position_edges
        
        position_dict=parent_object.position_dict(position_to_vertex=True)
        
        chord_edges=[]
        
        for position_edge in iter(position_edges):
            chord_edge=(position_dict[position_edge[0]],position_dict[position_edge[1]])
            chord_edges.append(chord_edge)
            
        return chord_edges
        
    
    def set_max_degree(self, max_degree=4):
        
        self.max_degree=max_degree
        return self.max_degree
    
    def set_parent_object(self, parent_object=None):
        
        self.parent_object=parent_object
        return self.parent_object
    
    #def set_chord_vector(self, chord_vector=None):
        
  #      if chord_vector is None or type(chord_vector) is tuple or type(chord_vector) is list:
 #           self.chord_vector=chord_vector
  #          return
            
  #      elif chord_vector.type is 'ChordVector':
 #           self.chord_vector=chord_vector.chord_vector
 #           self.set_parent_object(chord_vector.parent_object)
 #          return
        
 #       else:
 #           raise TypeError('chord_vector must be None or of type tuple, list, or ChordVector.')
    
    def position_dict(self, position_to_vertex=True):
        # This function calls self.parent_object.position_dict(), which returns
        #   a position to vertex dict if position_to_vertex=True, and a vertex
        #   to position dict otherwise.
        
        if self.parent_object is None: 
            raise MissingParentObject('ChordVector.position_dict requires calling self.parent_object.position_dict, but parent_object is None.')
        
        return self.parent_object.position_dict(position_to_vertex)
    
    
    def chord_vector(self, chord_edges=None, position_edges=None):
        
        # This function attempts to make a chord vector from either chord_edges
        #       or position_edges. chord_edges is with vertex labels, while
        #       position_edges is with positions. If a vertex/position has no
        #       incident edges, a 0 will be appended to the chord_vector to denote
        #       a skipped vertex.
        
        if position_edges is None: position_edges=self.position_edges
               
        positions_of_chords=self.positions_of_chords(chord_edges=chord_edges,
                                                     position_edges=position_edges)
        
        chord_vector=[]
        
        no_of_chords=len(positions_of_chords)
        no_of_positions=self.no_of_positions()
    
        for i in range(0,no_of_chords):
            difference_1=(positions_of_chords[i][1]-positions_of_chords[i][0])%no_of_positions
            difference_2=(positions_of_chords[i][0]-positions_of_chords[i][1])%no_of_positions
        
            if difference_1<=difference_2:
                chord_length=difference_1
            else:
                chord_length=-difference_2
                
            chord_vector.append(chord_length)
    
        return tuple(chord_vector)
    
    
    def positions_of_chords(self, chord_edges=None, position_edges=None):
        
        if position_edges is None: position_edges=self.position_edges
        
        if (chord_edges is None and position_edges is None): 
            if self.parent_object is None: 
                raise Underdefined('Exactly one of chord_edges, position_edges'
                                   ' must be defined.')
            else:
                edges=self.chord_edges()
                use_position_dict=True
        # At this point, one of chord_edges or position edges is defined, and
        #   self.parent_object is also defined.
            
        elif position_edges is None:
            position_dict=self.position_dict(position_to_vertex=True) # This is a position to vertex dict.
            use_position_dict=True
            edges=chord_edges
            
        elif chord_edges is None:
            use_position_dict=False
            edges=position_edges
        
        else:
            raise Overdefined('Exactly one of chord_edges, position_edges must be defined.')
        
        positions_of_chords=dict()
        chord_index=0
    
        for edge in iter(edges):
            u,v = edge[0], edge[1]
            
            if use_position_dict:
                position1, position2 = position_dict[u], position_dict[v]
                
            else:
                position1, position2 = u, v
                
            positions_of_chords[chord_index]=[position1,position2]
        
            chord_index+=1
            
        return positions_of_chords
