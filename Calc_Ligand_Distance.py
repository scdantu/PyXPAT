'''
Created on Jan 10, 2012
@author: Dhakeneswar
'''
pro_res=[222]

from numpy import linalg as LA
import PDB_Data as get_pdb_data
import Atom_Coordinates as at_cord
import Update_Pdb_List as update_pdb_list
import numpy as nump
import Global_Variables as gvariables
import Center_of_Mass as c_o_m

organism=[];    sequence=[];    
pdb_list=[];    dash_count=[];

def calculate_distance(org,seq,i_pdb_organism,i_pdb,i_pdbid,ihet_chain,ihet_compnd,ihet_index,c_start):
    global organism,sequence,pdb_list,dbref_chain_start
    lig_dist=gvariables.DUMMY
    pro_res=[223];
    #pro_res=[250];
    array_dist_data=[];
    dist_data=""; organism=org;sequence=seq;
    atom="CA";    pd="%s-%s-%s"%(i_pdbid,ihet_chain,ihet_compnd)    
    dist_data="%12s"%(pd)
    
    prores=pro_res[0];
    (pro_resAA,pro_res_index,dash_count)=get_pro_residues(i_pdb_organism,i_pdbid,i_pdb,prores)
    #print pro_resAA,pro_res_index,dash_count;
    #if(a_resAA!=gvariables.DUMMY):
    
    if(c_start<100):
        c_start=0
    if(c_start>100):
        c_start=c_start-1
    pro_res_index=pro_res_index+c_start
    (a)=get_ligand_coordinates(ihet_chain,ihet_compnd,ihet_index,i_pdb,dash_count)
    a_bad_vec=quality_check(a)
    #print a
    #S212
    b=get_coordinates(pro_resAA,pro_res_index,ihet_chain,i_pdb,atom,dash_count)
    b_bad_vec=quality_check(b)
    if(a_bad_vec==False)and(b_bad_vec==False):
        dist=LA.norm(a-b)
        lig_dist=dist;
        #dist_data="%12.3f"%(dist)
        dist_data+="%12.3f"%(dist)
        array_dist_data.append(dist_data)
        #array_dist_data.append(dist_data)
    if(a_bad_vec==True)or(b_bad_vec==True):
        #print "%12s %12s %12.3f %12s %12s"%(i_pdbid,ihet_chain,dist,a_resAA,a_res_index)
        dist_data="CRAP"
        print "%6s-%s %25s"%(i_pdbid,ihet_chain,"Bad Coordinates")
        dist_data=""
    #return array_dist_data,dist
    return dist_data,lig_dist

def get_ligand_coordinates(ihet_chain,ihet_compnd,ihet_index,i_pdb,dash_count):
    x_a=[];y_a=[];z_a=[];
    atom_type=[];
    x=gvariables.DUMMY;y=gvariables.DUMMY;z=gvariables.DUMMY;
    ihet_chain=ihet_chain.strip()
    fileOpen=open(i_pdb,"r")
    ires="";    ichain="";  iindex=0;
    for line in fileOpen:
        #split_line=line.split()
        atomrecord=line[0:6].strip()
        if(atomrecord=="HETATM"):
            ires=line[17:20]
            ires=ires.strip()
            ichain=line[21]
            iindex=line[22:27].strip()
            iindex=int(iindex)
            #print ires
        if(atomrecord=="HETATM")and(ires==ihet_compnd)and(ichain==ihet_chain)and(iindex==int(ihet_index)):
            Atom_Type=line[12:16].strip()
            x=line[30:38].strip();            
            y=line[38:46].strip();            
            z=line[46:54].strip()
            x=float(x);     y=float(y);     z=float(z);
            atom_type.append(Atom_Type);
            x_a.append(x);  y_a.append(y);  z_a.append(z);
    (avgx,avgy,avgz)=c_o_m.calc_com(atom_type,x_a,y_a,z_a)
    #(x,y,z,at_count)=at_cord.atom_coordinates(resAA,res_index,iChain,i_pdb,count,atom,dash_count)
    #x=float(x);y=float(y);z=float(z);
    vec=nump.array((avgx,avgy,avgz))
    return vec#,at_count

def quality_check(vec):
    bad_vec=False;
    for i in range(len(vec)):
        a=float(vec[i]);
        if(a==gvariables.DUMMY):#or(b==gvariables.DUMMY)or(c==gvariables.DUMMY):
            bad_vec=True;
    return bad_vec

def get_coordinates(resAA,res_index,iChain,i_pdb,atom,dash_count):
    count=0;
    (x,y,z,at_count)=at_cord.atom_coordinates(resAA,res_index,iChain,i_pdb,count,atom,dash_count)
    x=float(x);y=float(y);z=float(z);
    vec=nump.array((x,y,z))
    return vec#,at_count

def get_pro_residues(pdb_organism,pdbid,i_pdb_file,prodist):
    global organism,sequence,pdb_list
    count=organism.count(pdb_organism)
    a_resAA=gvariables.DUMMY;a_res_index=gvariables.DUMMY;
    if(count==0):
        print "Source not found for %s. Will not be analyzed further"%(pdbid)
        pdb_list=update_pdb_list.update_pdb_list(pdb_list,i_pdb_file)
    if(count>0):
        i_seq=organism.index(pdb_organism)
        seq=sequence[i_seq]
        (a_resAA,a_res_index,dash_count)=get_pdb_data.proc_sequence(seq,prodist)
        #(b_resAA,b_res_index,dash_count)=get_pdb_data.proc_sequence(seq,bdist)
    return a_resAA,a_res_index,dash_count