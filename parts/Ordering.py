#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 08:50:25 2018

@author: mohamed
"""

# =============================================================================
# This library could be imported via:
#   from k5descendants import Ordering
# =============================================================================


# =============================================================================
# class Ordering: 
# =============================================================================

class Ordering:

    type = 'Ordering'      # class variable shared by all instances
    
    def supported_orderings():
        return ['lex','revlex','grlex','revgrlex']
    
    def supported_modes(self):
        return ['unsorted','maximal','minimal']

    def __init__(self, ordering=None, mode=None):
        
        lexicographical, graded, reverse=False, False, False
            
        if not mode or mode=='unsorted':
            mode_name='Unsorted'
            
        elif mode in iter(self.supported_modes()):
            mode_name=mode[0].upper()+mode[1:]    
        
        if not ordering or ordering=='unordered':
            ordering_name='Unordered'
            mode_name=''
            lexicographical, graded, reverse=False, False, False
        
        elif not type(ordering)==str:
            raise TypeError('Argument of Ordering must be a string.')
            
        elif ordering=='lex':
            lexicographical, graded, reverse=True, False, False
            ordering_name='Lexicographical Ordering'
        
        elif ordering=='revlex':
            lexicographical, graded, reverse=True, False, True
            ordering_name='Reverse Lexicographical Ordering'
            
        elif ordering=='grlex':
            lexicographical, graded, reverse=True, True, False
            ordering_name='Graded Lexicographical Ordering'
            
        elif ordering=='revgrlex':
            lexicographical, graded, reverse=True, True, True
            ordering_name='Reverse Graded Lexicographical Ordering'
            
        else:
            raise ValueError('Unsupported ordering: '+ordering)
         
        self.name=mode_name+' '+ordering_name    
        self.is_lex=lexicographical
        self.is_graded=graded
        self.is_reverse=reverse
        self.ordering=ordering
        self.mode=mode
        
        self.ordering_name=ordering_name
        self.mode_name=mode_name