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
from numpy import linalg as LA
import PDB_Data as get_pdb_data
import Update_Pdb_List as update_pdb_list
import Atom_Coordinates as at_cord
import numpy as nump
import Global_Variables as gvariables
organism=[];sequence=[];pdb_list=[];dash_count=[];
a_dist=[180,187];b_dist=[223,223]

def calculate_distance(org,seq,nchains,chain_ids,i_pdb_organism,i_pdbid,i_pdb,het_chain,het_compnd):
    global organism,sequence,pdb_list,dbref_chain_start
    a_dist=[180,187];b_dist=[223,223]
    #a_dist=[207,214];b_dist=[250,250]
    dbref_chain_start=gvariables.dbref_chain_start;
    dist_data=""; organism=org;sequence=seq;
    atom="CA";
    array_dist_data=[];
    for i in range(nchains):
        iChain=str(chain_ids[i])
        iChain=iChain.strip()
        pd="%s-%s-%s"%(i_pdbid,iChain,het_compnd[i])
        dist_data="%12s"%(pd)
        for j in range(len(a_dist)):
            adist=a_dist[j];bdist=b_dist[j];
            (a_resAA,a_res_index,b_resAA,b_res_index,dash_count)=get_residues(i_pdb_organism,i_pdbid,i_pdb,adist,bdist)
            #print a_resAA,a_res_index,dash_count;
            #if(a_resAA!=gvariables.DUMMY):
            c_start=dbref_chain_start[i]
            if(c_start<100):
                c_start=0
            if(c_start>100):
                c_start=c_start-1
            a_res_index=a_res_index+c_start
            b_res_index=b_res_index+c_start
            (a)=get_coordinates(a_resAA,a_res_index,iChain,i_pdb,atom,dash_count)
            a_bad_vec=quality_check(a)
            b=get_coordinates(b_resAA,b_res_index,iChain,i_pdb,atom,dash_count)
            b_bad_vec=quality_check(b)
            if(a_bad_vec==False)and(b_bad_vec==False):
                dist=LA.norm(a-b)
                #print "%12s %12s %12.3f %12s %12s"%(i_pdbid,iChain,dist,a_resAA,a_res_index)
                dist_data+="%12.3f"%(dist)
                #array_dist_data.append(dist_data)
            if(a_bad_vec==True)or(b_bad_vec==True):
                #print "%12s %12s %12.3f %12s %12s"%(i_pdbid,iChain,dist,a_resAA,a_res_index)
                dist_data="CRAP"
                print "%6s-%s %25s"%(i_pdbid,iChain,"Bad Coordinates")
            if(a_bad_vec==False)and(j==len(a_dist)-1):
                array_dist_data.append(dist_data)
                dist_data=""
        #print dist_data
    return array_dist_data#,at_count
    #return dist_data
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
def get_residues(pdb_organism,pdbid,i_pdb_file,adist,bdist):
    global organism,sequence,pdb_list
    count=organism.count(pdb_organism)
    a_resAA=gvariables.DUMMY;a_res_index=gvariables.DUMMY;
    b_resAA=gvariables.DUMMY;b_res_index=gvariables.DUMMY;
    if(count==0):
        print "Source not found for %s. Will not be analyzed further"%(pdbid)
        pdb_list=update_pdb_list.update_pdb_list(pdb_list,i_pdb_file)
    if(count>0):
        i_seq=organism.index(pdb_organism)
        seq=sequence[i_seq]
        (a_resAA,a_res_index,dash_count)=get_pdb_data.proc_sequence(seq,adist)
        (b_resAA,b_res_index,dash_count)=get_pdb_data.proc_sequence(seq,bdist)
    return a_resAA,a_res_index,b_resAA,b_res_index,dash_count
