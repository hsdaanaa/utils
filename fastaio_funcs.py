#! usr/bin/env Python3
#===========================================================================
# Functions for reading and writing fasta files
# v251111a - by Hassan
#===========================================================================
#=============================Dependencies==================================
import sys
import os
import pandas as pd
import numpy as np
sys.path.append("./")
from iter_funcs import map_dict_vals
#==============================Reading functions============================
def fasta_to_dict(input_path):
    """takes an input path to a fasta file and delimiters between 
    an identifier, creates a dictionary with identifier: sequence"""
    
    cds_seq_dict = {}
    cds_names    = []
    with open(input_path, 'r') as file:
        for line in file:
            if line.startswith(">"):
                cds_name = line[1:]
                cds_name = cds_name.rstrip('\n')
                key = line[1:].rstrip('\n')
                cds_seq_dict[cds_name] = ''
                cds_names.append(cds_name)
            else:
                cds_seq_dict[cds_name] += line.rstrip('\n')
            
    assert len(cds_names) == len(cds_seq_dict), 'some sequences in the alignment had the same name.sequence names in alignment {}'.format(cds_names)
    return cds_seq_dict
#----------------------------------------------------------------------------
def scaffold_data_to_dict(input_path, delim1 ='>', comment_line = '#'): # change function name
    """"""
    descs = []
    seqs = []
    temp_line = []
    with open(input_path, 'r') as file:
        
            for line in file:
                if line.startswith(delim1):
                    descs.append(line.lstrip(delim1).rstrip('\n'))
                    if ''.join(temp_line) == '':
                        continue
                    else:
                        seqs.append(''.join(temp_line))
                    
                    temp_line = []
                elif line.startswith(comment_line):
                    continue
                else:
                    temp_line.append(line.replace('\n', ''))

            seqs.append(''.join(temp_line))
            
            return dict(zip(descs, seqs))
#----------------------------------------------------------------------------
def cds_files_to_dict(list_of_paths, delims_between_cds_name):
    """takes an input list of paths to fasta files 
    returns a nested dictionary in which the name of the file is 
    the key and the value is a nested dictionary of cds_name: cds_seq"""
    
    main_cds_dict = {}
    delim1 = delims_between_cds_name[0]
    delim2 = delims_between_cds_name[1]
    
    for path in list_of_paths:
        name = os.path.basename(path).rstrip('\n')
        cds_dict = fasta_to_dict[path]
        main_cds_dict[name] = cds_dict

    return main_cds_dict
#----------------------------------------------------------------------------
def cds_to_dataframe(paths, orient = 'columns'):

    for path in paths:
        cds_dict = fasta_to_dict(path)
        cds_dict = map_dict_vals(cds_dict, list)
        df = pd.DataFrame.from_dict(cds_dict, orient = orient) 
    
    return df
#==============================Writing functions=============================
def dict_to_fasta(dict_var, path_to_output_file, output_file_name):
    """outputs a dictionary to a fasta formatted file. cds names should be
    keys and values should be sequences"""

    # make file name
    file_name = os.path.join(path_to_output_file, output_file_name)
    # open file 
    file_obj = open(file_name, 'w')
     # loop over dictionary keys and writes cds_name/sequence lines.
    for cds_name in dict_var.keys():
            seq = ''.join(dict_var[cds_name]) # gets cds_sequence from dictionary of cds
            # writes data into file
            cds_name = cds_name.rstrip('\n')
            file_obj.write('>{}\n{}\n'.format(cds_name, seq))
            
    file_obj.close()
#----------------------------------------------------------------------------
