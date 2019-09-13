#!/usr/bin/python

'''
Created on Dec 14, 2011
@author: Dhakeneswar
'''
import Global_Variables as gvariables
ori_res_id=gvariables.DUMMY;
Atom_Type="";
def atom_coordinates(res_aa,resid,chain,i_pdb,count,atom,dash_count):
    global ori_res_id
    decrease=True;increase=False;
    found_coordinates=False
    limit=5;

    x=gvariables.DUMMY;y=gvariables.DUMMY;z=gvariables.DUMMY;
    if(count==0):
        store_res_id(resid,atom)
    #if(dash_count>10):
        #decrease=True;
        #count=limit;
    while(count<=limit)and(found_coordinates==False):
        #print count
        #print count,resid
        (x,y,z)=get_coordinates(i_pdb, res_aa, chain, count,resid)
        if(x!=gvariables.DUMMY):
            #count=gvariables.DUMMY
            found_coordinates=True
        if(count==limit)and(decrease==True):
            increase=True;decrease=False;
            count=1;
        if(count<limit)and(x==gvariables.DUMMY)and(decrease==True):
            count=count+1;
            resid=ori_res_id-count;
        if(count<=limit)and(x==gvariables.DUMMY)and(increase==True):
            count=count+1;
            resid=ori_res_id+count;
    return x,y,z,count

def get_coordinates(i_pdb,res_aa,chain,count,resid):
    global Atom_Type
    x=gvariables.DUMMY;y=gvariables.DUMMY;z=gvariables.DUMMY;
    resaa=gvariables.aa_dict(res_aa)
    fileOpen=open(i_pdb,"r")
    for line in fileOpen:
        split_line=line.split()
        if(split_line[0]=="ATOM")and(split_line[2]==Atom_Type)and(split_line[3]==resaa)and(split_line[4]==chain)and(int(split_line[5])==int(resid)):
            x=split_line[6].strip()
            y=split_line[7].strip()
            z=split_line[8].strip()
            break
    return x,y,z
def store_res_id(resid,atom):
    global ori_res_id,Atom_Type
    ori_res_id=resid
    Atom_Type=atom