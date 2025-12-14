#! usr/bin/env Python3
#===========================================================================
# Functions to for processing iterables such as strings, lists and tuples
# v251111a - by Hassan
#===========================================================================
#=============================Dependencies==================================
import sys
import os
import shutil
import decimal
import random
import copy
#==============================Functions====================================
def conv_nested_list_to_list(nlist_var, verbose = 0, none_if_error = True): 
    """takes an input list of lists (nested list). and 
    extracts all 'inner' list elements into the main list,
    making a 1 dimensional list.
    
    strategy
    --------
    -loops list and appends list items to a new list var.
    when the item is a list(inner list), the inner list is
    also looped and its items are appended to the new list. 
    
    parameters
    ----------
    nlist_var: list of list
        nested list to process
    verbose: 0,1
        optional parameter for debugging

    returns
    -------
    list"""

    # prints error message for invalid input
    try:
        assert isinstance(nlist_var, list)
    except:
        if none_if_error == True:
            return None
        else:
            print('your input was not a list')
    #check_input_type(list,'your input was not a list', nlist_var)
    
    new_list = [] # this allows appending items of list and inner list 
    
    
    # loops list and checks if each item is a list
    # if true, loops inner list and appends its elements to the new list
    # else, appends the items to the new list
    for item in nlist_var: 
        if isinstance(item, list) == True:
            items = conv_nested_list_to_list(item)
            new_list.extend(items)
        else:
            new_list.append(item)
            
        if verbose == 1: 
            print("current list item: {0}".format(item))
            
    if verbose == 1: 
        print('created list: {}'.format(new_list))

    return new_list
#---------------------------------------------------------------------------
def split_iterable(iterable, unit_len, verbose = 0): 
    """
    splits a sequnece of elements into chunks of N length.

    Process
    -------
    Divides count of elements in iterable by unit_len to get count of units.
    Loops unit_count number of times. 
        if unit count is 0, it returns a list with entire iterable.
        otherwise, the iterable is copied and a subset containing the first 
        unit_count elements is obtained. This subset is appended to a list and 
        the copied iterable is trimmed to exclude elements found in the appended 
        a list. The trimemd iterable is used for theh next loop.
    Checks whether iterable (after trimmings) still has elements. If so, the remaining
    elements are appended to a list.

    Parameters
    ----------
    iterable: examples are string, list, tuple
        a data type with elements
    unit_len: int
        number of elements in each chunk
    verbose: int 0, 1
        set to 1 for debugging output

    returns
    -------
    list"""

    out_seq_list  = [] 

    if verbose == 1:
        print("copying iterable")
    copy_iterable = copy.deepcopy(iterable)

    if verbose == 1: 
        print("calculating unit count")
    iterable_len    = len(copy_iterable)
    full_unit_count = int(iterable_len/unit_len) # note that this is floor division to get full units

    if full_unit_count == 0: 
        if verbose == 1: 
            print("full unit count is 0. So iterable will be added to list and returned")
        out_seq_list.append(copy_iterable)
        
    else:
        if verbose==1:
            print("full unit count is greater than 0. So starting loop")
        for time in range(0, full_unit_count): 
            if time == 0:
                seq_unit              = copy_iterable[:unit_len]
                mod_iterable_seq_line = copy_iterable[unit_len:]
                out_seq_list.append(seq_unit)
            else:
                seq_unit              = mod_iterable_seq_line[:unit_len]
                mod_iterable_seq_line = mod_iterable_seq_line[unit_len:]
                out_seq_list.append(seq_unit)
        if len(mod_iterable_seq_line)>0:
            out_seq_list.append(mod_iterable_seq_line)
        
    return out_seq_list
#---------------------------------------------------------------------------
def get_list_as_string(list_var, delimiter):
    """takes an input list and a delimiter and 
    a returns list elements separated by the delimiter
    """
    str_var = ''
    for index in range(len(list_var)): 
        element = list_var[index]
        if index == len(list_var)-1:
            str_var += '{}'.format(element)
        else:
            str_var += '{}{}'.format(element, delimiter)
            
    return str_var
#---------------------------------------------------------------------------
def remove_indices_from_list(list_var, indices):
    list_copy = copy.deepcopy(list_var)
    
    index_ordered = sorted(indices, reverse=True)
    
    for index in index_ordered:
        del list_copy[index]

    return list_copy
#--------------------------------------------
def merge_dicts(dict_one, dict_two):
    merged_dict = dict(list(dict_one.items()) + list(dict_two.items()))
    return merged_dict

#---------------------------------------------------------------------------
# function to loop over nested dictionary and modify key values 
def check_value_of_dict_key(input_dict, key, function):
    """takes an input dictionary and a key in the dictionary
    maps a functionto the value of the key and returns that 
    value"""
    
    output = map(input_dict[key], function) 
    
    return output
#---------------------------------------------------------------------------
def map_dict_vals(input_dict, func_name): 
    new_dict = {}
    
    for key in input_dict:
        value         = input_dict[key]
        new_value     = func_name(value)
        new_dict[key] = new_value
        
    return new_dict