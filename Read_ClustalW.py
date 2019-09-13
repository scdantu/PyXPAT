#!/usr/bin/python
'''
Created on Dec 1, 2011
@author: Dhakeneswar
'''
import re
#organism=[];        sequence=[];    
dash_count=[];
ORGANISM_SEQUENCE={};

dummy="CRAPPY";
store_seq=False;    temp_seq=dummy;
count=0;
def read_clustalW(fOpen):
    #global organism,sequence,store_seq
    global store_seq
    global temp_seq,count,dummy
    global ORGANISM_SEQUENCE
    temp_organism="";
    fileOpen=open (fOpen,"r");
    
    content=c=fileOpen.readlines();
    
    for i in range(len(content)):
        line=content[i]
        if(line[0]==">"):
            c=re.split('>|\n',line)
            s=c[1].strip()
            temp_organism=s.strip();
            #organism.append(s)
            #ORGANISM_SEQUENCE[s]=1;
            add_organism(temp_organism);
            store_seq=True;
        if(line[0]!=">"):
            #print line, len(line)
            l=re.split('\n|\r',line)
            #print l,len(line)
            #exit()
            if(count==0):
                temp_seq=l[0]
            if(count>0):
                temp_seq+=l[0]
            count=count+1
        if(temp_seq!="CRAPPY")and(count>0)and((line[0]==">")or (i==len(content)-1)):
                temp_seq=temp_seq.strip()
                #sequence.append(temp_seq)
                add_sequence(temp_organism,temp_seq)                
                count=0;
                temp_seq=dummy;
                store_seq=False
    #print get_hash_count()
    #return organism,sequence,dash_count
    return ORGANISM_SEQUENCE

def add_organism(organism):
    #org="";
    global ORGANISM_SEQUENCE,dummy
    if(ORGANISM_SEQUENCE.has_key(organism)==False):
        ORGANISM_SEQUENCE[organism]=dummy
    #if(ORGANISM_SEQUENCE.has_key(organism)==False):

def add_sequence(organism,sequence):
    global ORGANISM_SEQUENCE,dummy
    
    if(ORGANISM_SEQUENCE.has_key(organism)==True):
        ORGANISM_SEQUENCE[organism]=sequence
        
    if(ORGANISM_SEQUENCE.has_key(organism)==False):
        print "%s does not exist. Cant update sequence"%(organism);
        exit()
    
def get_hash_count():
    global sequence,dash_count
    dash_count=[];
    dash="-";
    for i in range(len(sequence)):
        seq=sequence[i]
        count=seq.count(dash)
        dash_count.append(count)
    return dash_count