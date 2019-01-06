#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:38:08 2018

@author: Mohamed Laradji
"""

class Overdefined(Exception):
    '''
    # Use when a function is called with too many parameters.
    '''
    
    pass


class Underdefined(Exception):
    '''
    # Use when a function is called with too few parameters.
    '''
    
    pass


class MissingParentObject(Exception):
    '''
    # Use when a function requires a defined parent object, but it is missing.
    '''
    
    pass


class NotSubgraph(Exception):
    '''
    # Use when a function on two graphs requires one of the graphs to be a subgraph of the other, but it isn't.
    '''
    
    pass


class AlreadyContained(Exception):
    '''
    # Use when adding an element to a set that already contains that element.
    '''
    
    pass 


class CannotBeAdded(Exception):
    '''
    # Use when an attempt to add an element to a set fails.
    '''
    
    pass 


class UnsupportedOption(Exception):
    '''
    # Use when an option is passed to a function that is not supported by that function.
    '''
    
    pass


class NotEndVertex(Exception):
    '''
    Use when an operation involving a vertex that is not an end vertex, but it needs to be.
    '''
    
    pass


class NotVertex(Exception):
    '''
    Use when an operation calls for a vertex that is not present.
    '''

    pass


class NoneReturned(Exception):
    '''
    Raised when a function returns None.
    '''
    
    pass

class InvalidHash(Exception):
    '''
    Raised when obtaining a value of an earlier version of an object.
    '''
    
    pass

class FileAlreadyExists(Exception):
    '''
    Raised when a file with the same name already exists, usually when attempting to save a file.
    '''
    
    pass


class FileDoesntExist(Exception):
    '''
    Raised when attempting to load a file that doesn't exist.
    '''
    
    pass


# class Unimplemented(Exception):
#     '''
#     Raised when a requested operation has not been implemented yet.
#     '''
    
#     pass