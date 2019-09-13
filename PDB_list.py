
'''
Created on Dec 6, 2011

@author: Dhakeneswar
'''
import fileIO.Write_1dData as w1d
import PDB_Data as pdb_data
import Update_Pdb_List as update_pdb_list
import General_Utilities as gen_util
FOLDER="/home/aklab/Projects/TIM/TIM-Analysis/pdbs";
FOLDER="/home/aklab/Projects/TIM/TIM-Analysis";

LOG_FOLDER="%s/log"%(FOLDER);

max_resolution=2.50; ORGANISM_SEQUENCE={};

gen_util.check_folder(LOG_FOLDER);

'''
HAS a BUG CANT access FOLDER variable from XPAT class

'''

def read_pdb_list(fOpen,org_seq):
    global pdb_list,ORGANISM_SEQUENCE
    
    ORGANISM_SEQUENCE=org_seq;
    
    fileOpen=open(fOpen,"r");
    list=fileOpen.readlines();
    
    pdb_list=[];
    
    for i in range(len(list)):
        pdb_list.append(list[i].strip("\n"));
    #print pdb_list
    (pdb_list,res_test)=chk_quality(pdb_list);
    
    #(pdb_list,chk_source)=chk_organism(pdb_list,clustal_organism)
    (pdb_list,chk_source)=chk_organism(pdb_list)
    return pdb_list,res_test,chk_source

def chk_organism(pdb_list):
    global ORGANISM_SEQUENCE,FOLDER
    org_test="Following PDB's will not be analyzed as the source organism sequence \nis not present in sequence alignment file\n";
    org_test+="%10s %60s\n"%("PDB ID","ORGANISM")    
    remove_list=[]
    
    '''
    Identify bad pdb's
    '''
    pdb_organism="";    is_present=False;    
    
    for i in range(len(pdb_list)):
        pdb_file="%s/pdbs/%s.pdb"%(FOLDER,pdb_list[i])
        
        gen_util.check_file(pdb_file);
        
        p=len(pdb_file)-8
        pdb=pdb_file[p:len(pdb_file)]
        
        pdb_organism=pdb_data.get_source(pdb_file)
        
        is_present=ORGANISM_SEQUENCE.has_key(pdb_organism),pdb_organism
        
        
        if(is_present[0]==False):
            org_test+="%10s %60s\n"%(pdb_list[i],pdb_organism)
            remove_list.append(pdb_list[i])
    for i in range(len(remove_list)):
        pdb_list.remove(remove_list[i])
    return pdb_list,org_test

def chk_quality(pdb_list):
    global max_resolution,LOG_FOLDER
    res_test="";    good_pdbs="";
    remove_list=[]
    '''
    Identify bad pdb's
    '''
    for i in range(len(pdb_list)):
        #pdb_file=pdb_list[i]
        pdb_file="%s/pdbs/%s.pdb"%(FOLDER,pdb_list[i])
        gen_util.check_file(pdb_file);

        p=len(pdb_file)-8
        pdb=pdb_file[p:len(pdb_file)-4]
        resolution=pdb_data.get_resolution(pdb_file)
        if(resolution<=max_resolution):
            good_pdbs+="%6s %8.3f\n"%(pdb,resolution)
        if(resolution>max_resolution):
            res_test+="%6s%s%6.3f\n"%(pdb,"\t did not pass resolution test. will not be used for analysis. \t",resolution)
            remove_list.append(pdb_list[i])
    fName="%s/XPAT-PdbResolution.dat"%(LOG_FOLDER)
    w1d.writeData(fName,good_pdbs)
    '''
    Remove bad pdb's
    '''
    for i in range(len(remove_list)):
        pdb_list.remove(remove_list[i])
    return pdb_list,res_test
