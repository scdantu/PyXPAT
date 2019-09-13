'''
Created on Jan 10, 2012

@author: Dhakeneswar
'''
import Global_Variables as gv
import numpy
import Hash_Maps as hash_maps
import Check_Atom as chk_atom
def calc_com(atom_array,x,y,z):
    x_len=len(x);
    mx=[];my=[];mz=[];mass=[];
    avg_x=gv.DUMMY;     avg_y=gv.DUMMY;     avg_z=gv.DUMMY;
    for i in range(x_len):
        atom=atom_array[i];     atom=atom.strip();
        i_x=float(x[i]);    i_y=float(y[i]);    i_z=float(z[i]);
        atom=chk_atom.check_atom(atom)
        i_mass=hash_maps.atom_mass(atom)
        imx=i_mass*i_x;     imy=i_mass*i_y;     imz=i_mass*i_z;
        mx.append(imx);     my.append(imy);     mz.append(imz);
        mass.append(i_mass)
    
    sum_mass=numpy.sum(mass)
    avg_x=numpy.sum(mx)/sum_mass;
    avg_y=numpy.sum(my)/sum_mass;
    avg_z=numpy.sum(mz)/sum_mass;
    return avg_x,avg_y,avg_z