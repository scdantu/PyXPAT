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
import numpy
import Global_Variables as gv
import re as reg_exp
import Calc_Ligand_Distance as calc_lig_dist
def get_resolution(fOpen):
    resolution=gv.DUMMY;
    fileOpen=open(fOpen,"r")
    for line in fileOpen:
        split_line=line.split()
        if(len(split_line)==5):
            #print split_line
            if(split_line[0]=="REMARK")and(split_line[1]=="2")and(split_line[2]=="RESOLUTION."):
                resolution=float(split_line[3])
                break
    return resolution
def get_general_info(fOpen):
    num_chains=gv.DUMMY;organism="";
    dbref_chain=[];dbref_start=[];dbref_end=[];
    chain_ids=[];c=[];
    het_chain=[];   het_compnd=[];  het_index=[];
    fileOpen=open(fOpen,"r")
    for line in fileOpen:
        split_line=line.split()
        if(split_line[0]=="COMPND")and(split_line[1]=="3")and(split_line[2]=="CHAIN:"):
            temp=line[18:80].strip()
            c=reg_exp.split(',|;',temp)
            num_chains=len(c)-1
        if(split_line[0]=="SOURCE")and(split_line[1]=="2")and(split_line[2]=="ORGANISM_SCIENTIFIC:"):
            temp=line[32:80].strip()
            org=reg_exp.split(';',temp)
            organism=org[0]
            #print organism
        if(split_line[0]=="HET")and(len(split_line)>=4):
            hetcompnd=line[7:10].strip()#split_line[1]
            hetchain=line[12]
            hetindex=line[13:17].strip()#split_line[3]
            het_chain.append(hetchain)
            het_compnd.append(hetcompnd)
            het_index.append(hetindex)
        if(split_line[0]=="DBREF"):
            dbchain=split_line[2]
            dbchain=str(dbchain[0])
            dchain=dbchain[0]
            dchain=dchain.strip()
            chain_start=int(split_line[3])
            chain_end=int(split_line[4])
            dbref_chain.append(dchain)
            dbref_start.append(chain_start)
            dbref_end.append(chain_end)  
    if(len(c)>=1):
        for i in range(len(c)-1):
            ic=c[i]
            ic=ic.strip()
            chain_ids.append(ic)
    dbref_proc(chain_ids,dbref_chain,dbref_start,dbref_end)
    #return num_chains,chain_ids,organism,dbref_chain,dbref_start,dbref_end
    #(het_chain,het_compnd)=process_ligand(organism,het_chain,het_compnd,num_chains,chain_ids)
    return num_chains,chain_ids,organism,het_chain,het_compnd,het_index
def chk_lig_dist(modchain,modcompnd,lig_dist_list,ihet_chain,ihet_compnd,lig_dist):
    #addligand=False;
    count=modchain.count(ihet_chain)
    if(count==0):
        #addligand=True;
        modchain.append(ihet_chain)
        modcompnd.append(ihet_compnd)
        lig_dist_list.append(lig_dist)
    if(count>=1):
        index=modchain.index(ihet_chain)
        olddist=lig_dist_list[index]
        if(olddist>lig_dist):
            modcompnd[index]=ihet_compnd
            lig_dist_list[index]=lig_dist
    return modchain,modcompnd,lig_dist_list
def process_ligand(organism,sequence_Array,pdb_organism,pdbid,i_pdb,nchains,chain_ids,het_chain,het_compnd,het_index,num_chains):
    modchain=[];modcompnd=[];
    lig_dist_data="";   lig_dist_list=[];
    dbref_chain_start=gv.dbref_chain_start;
    dbref_chain=[];
    num_compnds=len(het_compnd)
    limit=8.00;
    for i in range(nchains):
        dbref_chain.append(chain_ids[i])

    for i in range(num_compnds):
        ihet_index=int(het_index[i])
        ihet_compnd=het_compnd[i]
        ihet_chain=het_chain[i]
        ihet_chain=ihet_chain.strip()
        if(ihet_compnd!="APO"):
            dbc_index=dbref_chain.index(ihet_chain)
            db_c_start=int(dbref_chain_start[dbc_index])
            (dist_data,lig_dist)=calc_lig_dist.calculate_distance(organism,sequence_Array,pdb_organism,i_pdb,pdbid,ihet_chain,ihet_compnd,ihet_index,db_c_start)
            lig_dist_data+="%s\n"%(dist_data)
            
            
            if(lig_dist<limit):
                modchain.append(ihet_chain)
                modcompnd.append(ihet_compnd)
                lig_dist_list.append(lig_dist)       
            if(lig_dist>limit):
                modchain.append(ihet_chain)
                modcompnd.append("APO")
                lig_dist_list.append(lig_dist)
        if(ihet_compnd=="APO"):
            modchain.append(ihet_chain)
            modcompnd.append(ihet_compnd)
            
    #print modchain
    #print modcompnd
    #print modchain
    #print modcompnd
    #print lig_dist_list
    mchain=[];mcompnd=[];hcount=0;
    for i in range(nchains):
        cid=chain_ids[i]
        nc=modchain.count(cid)
        
        if(nc==1):
            mchain.append(chain_ids[i])
            mcompnd.append(modcompnd[hcount])
            hcount=hcount+1;
        if(nc==0):
            mchain.append(chain_ids[i])
            mcompnd.append("APO")

        if(nc>1):
            count=nc;   j=0;
            jindex=modchain.index(chain_ids[i])
            j_dist=[];j_lig=[];
            while(j<len(modchain)):
                jchain=modchain[j]
                if(jchain==cid):
                    j_dist.append(float(lig_dist_list[j]))
                    j_lig.append(modcompnd[j])
                j=j+1;
            min=numpy.min(j_dist)
            chk_lig=""
            if(min<limit):
                idex=j_dist.index(min)
                chk_lig=j_lig[idex]
            if(min>=limit):
                chk_lig="APO"
            mchain.append(chain_ids[i])
            mcompnd.append(chk_lig)

            '''
            for j in range(count):
                j_lig=chk_ligand(het_compnd[jindex+j])
                temp_chk_lig.append(j_lig);
                #print temp_chk_lig
            temp_count=temp_chk_lig.count("APO")
            if(temp_count==count):
                chk_lig="APO"
            if(temp_count<count):
                for n in range(count):
                    j_lig=temp_chk_lig[n]
                    if(j_lig!="APO"):
                        chk_lig=j_lig
                #chk_lig=chk_ligand(het_compnd[hcount])
            mchain.append(chain_ids[i])
            mcompnd.append(chk_lig)
            '''
    #print mchain
    #print mcompnd
    return mchain,mcompnd,lig_dist_data
    #return modchain,modcompnd,lig_dist_data
def proc_ligand(het_chain,het_compnd,num_chains,chain_ids):
    modchain=[];modcompnd=[];
    if(num_chains>len(het_chain)):
        hcount=0;
        for i in range(num_chains):
            count=het_chain.count(chain_ids[i])
            #print chain_ids[i],count
            if(count==0):
                modchain.append(chain_ids[i])
                modcompnd.append("APO")
            if(count==1):
                modchain.append(chain_ids[i])
                chk_lig=chk_ligand(het_compnd[hcount])
                modcompnd.append(chk_lig)
                hcount=hcount+1;
    if(num_chains<len(het_chain)):
        hcount=0;
        for i in range(num_chains):
            temp_chk_lig=[];
            count=het_chain.count(chain_ids[i])
            if(count>1):
                temp_chk_lig=[];
                jindex=het_chain.index(chain_ids[i])
                for j in range(count):
                    j_lig=chk_ligand(het_compnd[jindex+j])
                    temp_chk_lig.append(j_lig);
                #print temp_chk_lig
                temp_count=temp_chk_lig.count("APO")
                if(temp_count==count):
                    chk_lig="APO"
                if(temp_count<count):
                    for j in range(count):
                        j_lig=temp_chk_lig[j]
                        if(j_lig!="APO"):
                            chk_lig=j_lig
                #chk_lig=chk_ligand(het_compnd[hcount])
                modchain.append(chain_ids[i])
                modcompnd.append(chk_lig)
                #hcount=hcount+1
            if(count==1):
                modchain.append(chain_ids[i])
                chk_lig=chk_ligand(het_compnd[hcount])
                modcompnd.append(chk_lig)
                hcount=hcount+1
    return modchain,modcompnd
def chk_ligand(hetcompnd):
    het="APO"
    #libraryHolo=/["2PG","3PG","13P","3PP","RES","PGH","PGA","G3P","G3H","G2H","CIT","X1S","X1R","SO4","4PB","BBR","NO3","PO4","129"];
    libraryHolo=["129","2PG","3PG","13P","3PP","RES","PGH","PGA","G3P","G3H","G2H","CIT","BBR","PO4","X1S","X1R","S04","NO3"];
    #for i in range(len_lib):
    hetcompnd=hetcompnd.strip()
    count=libraryHolo.count(hetcompnd)
    if(count==0):
        het="APO"
    if(count==1):
        index=libraryHolo.index(hetcompnd)
        het=libraryHolo[index]
    return het
def get_source(fOpen):
    organism="";
    fileOpen=open(fOpen,"r")
    for line in fileOpen:
        split_line=line.split()
        if(split_line[0]=="SOURCE")and(split_line[1]=="2")and(split_line[2]=="ORGANISM_SCIENTIFIC:"):
            temp=line[32:80].strip()
            org=reg_exp.split(';',temp)
            organism=org[0]
            #print organism
    return organism

def dbref_proc(chain_ids,dbref_chain,dbref_start,dbref_end):
    numchains=len(chain_ids)
    chain_start=[];chain_end=[];
    for i in range(numchains):
        if(i<len(dbref_chain)):
            iChain=chain_ids[i]
            iChain=iChain.strip()
            chain_count=dbref_chain.count(iChain)
            i_index=dbref_chain.index(iChain)
            if(chain_count>1):
                start=dbref_start[i_index];
                end=dbref_end[i_index+chain_count-1];
                chain_start.append(start)
                chain_end.append(end)
            if(chain_count==1):
                start=(dbref_start[i]);
                end=dbref_end[i];
                chain_start.append(start)
                chain_end.append(end)
    gv.dbref_mod_chain_num(chain_start, chain_end)
def proc_sequence(seq,ori_index):
    dash="-";
    if(ori_index>0):
        seq=seq.strip()
        dash_count=0;
        for i in range(len(seq)):      
            if(i==(ori_index-1)):
                resAA=seq[i]
                mod_index=ori_index-dash_count
                #print mod_index,dash_count,ori_index
                break;
            if(seq[i]==dash):
                dash_count=dash_count+1;
        #print resAA,mod_index;
    #print dash_count
    return resAA,mod_index,dash_count
