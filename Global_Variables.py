'''
Created on Dec 6, 2011

@author: Dhakeneswar
'''
import numpy as nump
DUMMY=99999
dbref_chain_start=[];
dbref_chain_end=[];
def dbref_mod_chain_num(dbcs,dbce):
    global dbref_chain_end,dbref_chain_start
    dbref_chain_start=dbcs;
    dbref_chain_end=dbce;
def return_vector(x,y,z):
    x=float(x)
    y=float(y)
    z=float(z)
    vector=nump.array((x,y,z))
    return vector
def mod_dihed_indice(dihed_indice):
    temp=[];
    for i in range(len(dihed_indice)):
        indice=int(dihed_indice[i])
        if(i==0):
            temp.append(indice-1)
        temp.append(indice)
        if(i==len(dihed_indice)-1):
            temp.append(indice+1)
    dihed_indice=temp
    return dihed_indice

def return_pdbid(pdb_file_location):
    p=len(pdb_file_location)-8
    pdbid=pdb_file_location[p:len(pdb_file_location)-4]
    return pdbid
    
def aa_dict(aa):
    aadict = {
        "A": "ALA",
        "R": "ARG",
        "N": "ASN",
        "D": "ASP",
        "C": "CYS",
        "Q": "GLN",
        "E": "GLU",
        "G": "GLY",
        "H": "HIS",
        "I": "ILE",
        "L": "LEU",
        "K": "LYS",
        "M": "MET",
        "F": "PHE",
        "P": "PRO",
        "S": "SER",
        "T": "THR",
        "W": "TRP",
        "Y": "TYR",
        "V": "VAL", 
        }
    return aadict[aa]