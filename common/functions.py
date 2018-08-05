#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 13:34:47 2018

@author: Mohamed Laradji
"""


# =============================================================================


import exceptions as exc


# =============================================================================


def convert_to_iterable(thing = None, raise_None_exception = True):
    '''
    Attempts to return an iterable version of thing. Raises a TypeError if it is not possible.
    '''
    
    if thing is None:
        if raise_None_exception: 
            raise exc.NoneReturned('thing is None.')

    else:
        try:
            thing = iter(thing)
            
        except TypeError:
            try:
                thing = iter([thing])
                
            except TypeError:
                raise TypeError('Unknown error.')
                
    return thing

# =============================================================================


def num_print(number, value, separator = ') '):
    '''
    Prints number and then value. 
    '''
    
    print(str(number) + separator + str(value))
    
# =============================================================================

def autonum_print(value, separator = ') ', reset_num = False):
    '''
    Prints a number, obtained from the global variable number_print, and then value.
    '''
    
    global print_number
    
    if reset_num:
        print_number = 1
    
    try:
        num_print(print_number, value, separator = separator)
        print_number += 1
        
    except NameError:
        autonum_print(value, separator = separator, reset_num = True)
        

# =============================================================================


def save(file, filename, extension = None, path = None, overwrite = False):
    '''
    Function save(file, filename, **kwargs): object, str, str -> None

    Saves file to disk. Returns without output if succesful. 
    
    Note that save requires both the pickle and dill modules to be installed.

    Options:
        extension - str -   The extension to append to filename. If None, no extension is appended.
        path -      str -   The location to which the file should be saved. If unspecified, saves to "../data/".
        overwrite - bool -  Default: False. If True, overwrites the preexisting files. If False, raises a FileAlreadyExists exception if a file with the same name already exists.
    '''

    import pickle
    import dill # dill is helpful in pickling lambda functions. Attempting to save lambda functions without dill raises an error.

    if path is None:
        path="../data/"
        
    if extension is None:
        extension = ""
    
    else:
        extension = "." + extension
        
    fullfilename = path + filename + extension
    
    if not overwrite:
        
        import os.path
        
        if os.path.isfile(fullfilename):
            
            raise exc.FileAlreadyExists('A file already exists on ' + fullfilename + '. Either try a different filename or set overwrite to True.')
            

    with open(fullfilename, "w") as f:
        pickle.dump(file, f, pickle.HIGHEST_PROTOCOL)

    return


# =============================================================================

    
def load(filename, extension = None, path = None):
    '''
    Function load(filename, **kwargs): str, str -> None

    Loads file from disk. Returns the file if successful, and raises an exception otherwise. 
    
    Note that loads requires both the pickle and dill modules to be installed.

    Options:
        extension - str -   The extension to append to filename. If None, no extension is appended.
        path -      str -   The location from which the file should be loaded. Default: "../data/".
    '''

    import pickle
    import dill # dill is helpful in pickling lambda functions. Attempting to save lambda functions without dill raises an error.

    if path is None:
        path="../data/"
        
    if extension is None:
        extension = ""
        
    fullfilename = path+filename+extension
    
    import os.path
        
    if not os.path.isfile(fullfilename):
            
        raise exc.FileDoesntExist('The requested file on ' + fullfilename + ' does not exist.')
            

    with open(fullfilename, "r") as f:
        file = pickle.load(f)

    return file

# =============================================================================