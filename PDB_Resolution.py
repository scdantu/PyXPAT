'''
Created on Dec 6, 2011

@author: Dhakeneswar
'''
import Global_Variables as gv
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
def get_num_chains(fOpen):
    num_chains=gv.DUMMY;
    chain_ids=[]
    fileOpen=open(fOpen,"r")
    for line in fileOpen:
        split_line=line.split()
        if(len(split_line)==5):
            #print split_line
            if(split_line[0]=="REMARK")and(split_line[1]=="2")and(split_line[2]=="RESOLUTION."):
                num_chains=float(split_line[3])
                break
    return num_chains,chain_ids

