'''
Created on Jan 10, 2012

@author: Dhakeneswar
'''
def check_atom(atom):
    mod_atom="C"
    atom=atom.upper()
    if(atom[0]=="H"):
        mod_atom="H"
    elif(len(atom)==2)and(atom[0]=="N")and(atom[1]=="A"):
        mod_atom="Na";
    elif(atom[0]=="C")and(len(atom)==2)and(atom[1]!="L")and(atom[1]!="A"):
        mod_atom="C";
    elif(atom[0]=="C")and(len(atom)==1):
        mod_atom="C";

    elif(atom[0]=="N"):
        if(len(atom)==1):
            mod_atom="N";
        if(len(atom)==2):
            if(atom[0]=="N")and(atom[1]!="A"):
                mod_atom="N";
    elif(atom[0]=="O"):
        mod_atom="O";
    elif(atom[0]=="S"):
        mod_atom="S";
    elif(atom[0]=="M")and(atom[1]=="N"):
        mod_atom="Mn";
    elif(atom[0]=="M")and(atom[1]=="G"):
        mod_atom="Mg";
    elif(atom[0]=="P"):
        mod_atom="P";
    elif(atom[0]=="C")and(len(atom)==2)and(atom[1]=="L"):
        mod_atom="Cl";
    elif(atom[0]=="C")and(len(atom)==2)and(atom[1]=="A"):
        mod_atom="Ca";
    return mod_atom;