'''
Created on Jan 10, 2012
@author: Dhakeneswar
'''
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
def atom_mass(atom):
    atommass = {
        "H":1.008,
        "C":12.01,
        "N":14.0067,
        "O":16.001,
        "S":32.065,
        "P":30.97,
        "Na":22.989,
        "Mg":24.3050,
        "Cl":35.453,
        "Ca":40.078,
    }
    return atommass[atom]