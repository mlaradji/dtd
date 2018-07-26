#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 13:34:47 2018

@author: Mohamed Laradji
"""

from exceptions import NoneReturned

def convert_to_iterable(thing = None, raise_None_exception = True):
    '''
    Attempts to return an iterable version of thing. Raises a TypeError if it is not possible.
    '''
    
    if thing is None:
        if raise_None_exception: 
            raise NoneReturned('thing is None.')

    else:
        try:
            thing = iter(thing)
            
        except TypeError:
            try:
                thing = iter([thing])
                
            except TypeError:
                raise TypeError('Unknown error.')
                
    return thing


def num_print(number, value, separator = ') '):
    '''
    Prints number and then value. 
    '''
    
    print(str(number) + separator + str(value))