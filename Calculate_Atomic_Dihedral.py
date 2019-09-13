#!/usr/bin/python
'''
    @release_date  : $release_date
    @version       : $release_version
    @author        : Sarath Chandra Dantu
    

     Copyright (C) 2011-2019 Sarath Chandra Dantu 

     This file is part of: XPAT

     XPAT is a free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     XPAT is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with XPAT.  If not, see <http://www.gnu.org/licenses/>.

'''
import Global_Variables as gvariables
import PDB_Data as get_pdb_data
import Update_Pdb_List as update_pdb_list
import Atom_Coordinates as at_cord
import DihedralCalculator as dih_Calc
a_res_index=0;
organism=[];sequence=[];pdb_list=[];dash_count=[];
dihed_indice=[];res_indice=[];
#dbref_chain_end=gvariables.dbref_chain_end;
phi_atom=["C","N","CA","C"];
psi_atom=["N","CA","C","N"];
def calculate_dihedral(org,seq,nchains,chain_ids,i_pdb_organism,i_pdbid,i_pdb,het_chain,het_compnd):
    global organism,sequence,pdb_list,res_indice
    global phi_atom,psi_atom,a_res_index
    global dihed_indice,dbref_chain_start
    dihed_indice=[220,221,222,223,224,225];
    #dihed_indice=[247,248,249,250,251,252];
    temp_data="";dihed_data="";array_dihed_data=[]; 
    organism=org;sequence=seq;
    dbref_chain_start=gvariables.dbref_chain_start;
    dihed_indice=gvariables.mod_dihed_indice(dihed_indice)
    pdbid=gvariables.return_pdbid(i_pdb)
    (resAA,res_indice,dash_count)=get_residues(i_pdb_organism,i_pdbid,i_pdb)
    num_dihed=len(resAA)-2;
    for i in range(len(chain_ids)):
        iChain=str(chain_ids[i])
        iChain=iChain.strip()
        pd="%s-%s-%s"%(pdbid,iChain,het_compnd[i])    
        i_c_p="%12s"%(pd)
        for j in range(num_dihed):
            a_j=j+1;
            a_resAA=resAA[j+1];            a_res_index=res_indice[j+1]
            '''
            DBREF CHAIN ID CORRECTION
            incase chainB,C,D.... starts with other than 1
            '''
            c_start=dbref_chain_start[i]
            if(c_start<100):
                c_start=0
            if(c_start>100):
                c_start=c_start-1
            a_res_index=a_res_index+c_start
            
            a=get_phi_coordinates(resAA,a_j,a_resAA,iChain,i_pdb,phi_atom,dash_count)
            a_bad_vec=quality_check(a)
            if(a_bad_vec==False):
                if(j==0):
                    temp_data="%6s"%(i_c_p)
                dihedral_angle=dih_Calc.CalcDihedralAngle(a)
                temp_data+="%10.2f"%(dihedral_angle)
            if(a_bad_vec==True):
                print "%6s-%s %25s"%(i_pdbid,iChain,"DHA Bad Phi Coordinates")
            a=get_psi_coordinates(resAA,a_j,a_resAA,iChain,i_pdb,psi_atom,dash_count)
            a_bad_vec=quality_check(a)
            if(a_bad_vec==False):
                dihedral_angle=dih_Calc.CalcDihedralAngle(a)
                temp_data+="%10.2f"%(dihedral_angle)
            if(a_bad_vec==True):
                print "%6s-%s %25s"%(i_pdbid,iChain,"DHA Bad Psi Coordinates")
            if(a_bad_vec==False)and(j==num_dihed-1):
                #temp_data+="\n"
                array_dihed_data.append(temp_data)
    #dihed_data=temp_data
    #return dihed_data,array_dihed_data
    return array_dihed_data
def get_phi_coordinates(resAA,a_j,a_resAA,iChain,i_pdb,phi_atom,dash_count):
    global a_res_index
    count=0;
    phi_coordinates=[[1000]*3,[1000]*3,[1000]*3,[1000]*3,[1000]*3]
    for i in range(len(phi_atom)):
        atom=phi_atom[i]
        if(atom=="C")and(i==0):
            i_index=a_res_index-1;
            prev_res=resAA[a_j-1]
            (x,y,z,at_count)=at_cord.atom_coordinates(prev_res,i_index,iChain,i_pdb,count,atom,dash_count)
            #print "%6s%6s%6d%6d"%(atom,prev_res,at_count,i_index)
            '''
            if res index is off by 'at_count'
            each value of input 'res_index' array has to be offset by 'at_count'
            and also a_res_index has to be adjusted using at_count 
            '''
            if(at_count>0):
                mod_res_index(at_count)
                #print "old\t",i_index
                i_index=i_index-at_count;
                a_res_index=a_res_index-at_count
                (x,y,z,at_count)=at_cord.atom_coordinates(prev_res,i_index,iChain,i_pdb,count,atom,dash_count)
                #print i_index,"\tnew\t",at_count
            x=float(x);y=float(y);z=float(z);
            phi_coordinates[i][0]=x;phi_coordinates[i][1]=y;phi_coordinates[i][2]=z;
            #print "%5s%4d%4s%12.3f%12.3f%12.3f"%(prev_res,i_index,atom,x,y,z)
        if(i>0):
            (x,y,z,at_count)=at_cord.atom_coordinates(a_resAA,a_res_index,iChain,i_pdb,count,atom,dash_count)
            x=float(x);y=float(y);z=float(z);
            phi_coordinates[i][0]=x;phi_coordinates[i][1]=y;phi_coordinates[i][2]=z;
            #print "%5s%4d%4s%12.3f%12.3f%12.3f"%(a_resAA,a_res_index,atom,x,y,z)
    return phi_coordinates

def get_psi_coordinates(resAA,a_j,a_resAA,iChain,i_pdb,psi_atom,dash_count):
    global a_res_index
    count=0;
    psi_coordinates=[[1000]*3,[1000]*3,[1000]*3,[1000]*3,[1000]*3]
    for i in range(len(psi_atom)):
        atom=psi_atom[i]
        if(atom=="N")and(i==3):
            i_index=a_res_index+1;
            prev_res=resAA[a_j+1]
            (x,y,z,at_count)=at_cord.atom_coordinates(prev_res,i_index,iChain,i_pdb,count,atom,dash_count)
            x=float(x);y=float(y);z=float(z);
            psi_coordinates[i][0]=x;psi_coordinates[i][1]=y;psi_coordinates[i][2]=z;
            #print "%5s%4d%4s%12.3f%12.3f%12.3f"%(prev_res,i_index,atom,x,y,z)
        if(i<3):
            #i_index=res_index-1
            (x,y,z,at_count)=at_cord.atom_coordinates(a_resAA,a_res_index,iChain,i_pdb,count,atom,dash_count)
            x=float(x);y=float(y);z=float(z);
            psi_coordinates[i][0]=x;psi_coordinates[i][1]=y;psi_coordinates[i][2]=z;
            #print "%5s%4d%4s%12.3f%12.3f%12.3f"%(a_resAA,a_res_index,atom,x,y,z)
            #vec=nump.array((x,y,z))
    return psi_coordinates
def get_residues(pdb_organism,pdbid,i_pdb_file):
    global organism,sequence,pdb_list
    global dihed_indice
    resAA=[];res_indice=[];
    count=organism.count(pdb_organism)
    if(count==0):
        print "Source not found for %s. Will not be analyzed further"%(pdbid)
        pdb_list=update_pdb_list.update_pdb_list(pdb_list,i_pdb_file)
    if(count>0):
        i_seq=organism.index(pdb_organism)
        seq=sequence[i_seq]
        for i in range(len(dihed_indice)):
            (i_resAA,i_res_indice,dash_count)=get_pdb_data.proc_sequence(seq,dihed_indice[i])
            resAA.append(i_resAA)
            res_indice.append(i_res_indice)
    return resAA,res_indice,dash_count
def mod_res_index(at_count):
    global res_indice
    mod_indice=[];
    for i in range(len(res_indice)):
        modres=int(res_indice[i])-at_count
        mod_indice.append(modres)
    res_indice=mod_indice
def quality_check(vec):
    bad_vec=False;
    x_len=len(vec)
    y_len=len(vec[0])
    for i in range(x_len):
        for j in range(y_len):
            a=float(vec[i][j]);#b=float(vec[1]);c=float(vec[2]);
            if(a==gvariables.DUMMY):#or(b==gvariables.DUMMY)or(c==gvariables.DUMMY):
                bad_vec=True;
    return bad_vec
