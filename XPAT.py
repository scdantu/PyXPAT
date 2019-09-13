'''
v1.5 11.11.2016
@author: Dhakeneswar
IMPLEMENTED CALCULATION OF LIGAND+S212 DISTANCE
X-ray Resolution
'''

#import Parse_Options as poptions
import Read_ClustalW as readcw;
import sys,time
import PDB_list as pdblist
import PDB_Data as get_pdb_data
import Global_Variables as gvariables
import Calculate_Atomic_Distance as calc_atomic_dist
import Calculate_Atomic_Dihedral as calc_atomic_dihe
import Analysis_Stats as ana_stats
import fileIO.Write_1dData as w1d

import General_Utilities as gen_util
Calc_Dist=True;     Calc_Dihedral=True;
#folder="C:\\Users\\Dhakeneswar\\Desktop\\ensemble"

FOLDER="/home/aklab/Projects/TIM/TIM-Analysis";
LOG_FOLDER="%s/log"%(FOLDER);

ORGANISM_SEQUENCE={};

organism=[];    sequence=[];    pdb_list=[];    dash_count=[];
dist_pdbid=[];  fin_dist=[];    fin_dihed=[];

def main(pdb_files_list):
    analysis_controller(pdb_files_list)
def analysis_controller(pdb_files_list):
    get_sequence()
    
    get_pdb_list(pdb_files_list)
    exit()
    #proc_pdb_list()
    
def get_pdb_list(pdb_files_list):
    global FOLDER,LOG_FOLDER,ORGANISM_SEQUENCE
    
    global pdb_list,organism
    fOpen="%s/%s"%(FOLDER,pdb_files_list);
    print fOpen
    gen_util.check_file(fOpen);
    (pdb_list,res_test,org_test)=pdblist.read_pdb_list(fOpen,ORGANISM_SEQUENCE)

    print res_test
    print org_test

    fName="%s/XPAT-Log.dat"%(LOG_FOLDER)
    data="%s\n%s"%(res_test,org_test)
    w1d.writeData(fName, data)
    exit()

def get_sequence():
    #global organism,sequence,dash_count,FOLDER
    global FOLDER,ORGANISM_SEQUENCE
    cwfname="%s/aln/ClustalW2-TIM.aln"%(FOLDER)
    gen_util.check_file(cwfname)
    ORGANISM_SEQUENCE=readcw.read_clustalW(cwfname);
    
    
def proc_pdb_list():
    global pdb_list,ORGANISM_SEQUENCE
    global dist_pdbid,fin_dist,fin_dihed
    global Calc_Dihedral,Calc_Dist
    dist_data="";dihed_data="";
    
    lig_dist_data="*** Ligand Distance with S212 ***\n";    
    num_pdbs=len(pdb_list)
    t_n_chains=0;
    #Calc_Dihedral=False;Calc_Dist=False;
    print "Number of PDB's to process: %12d"%(num_pdbs)
    if(num_pdbs==0):
        Calc_Dihedral=False;Calc_Dist=False;
    for i in range(num_pdbs):
    #for i in range(0,10):        
        i_pdb=pdb_list[i]
        pdbid=gvariables.return_pdbid(i_pdb)
        print "Processing PDB: %12d%12s"%(i+1,pdbid)
        #sys.stdout.write("\r{0}".format(print_t))
        #sys.stdout.flush()
        #time.sleep(0.0)
        (nchains,chain_ids,pdb_organism,het_chain,het_compnd,het_index)=get_pdb_data.get_general_info(i_pdb)
        #print het_chain
        #print het_compnd
        nchains=int(nchains);
        t_n_chains=t_n_chains+nchains;
        c_h_chain=len(het_chain);
        if(c_h_chain==0):
            lig_dist_data+="%12s%20s\n"%(pdbid,"NO HET COMPOUNDS")
            for j in range(nchains):
                het_chain.append(chain_ids[j])
                het_compnd.append("APO")
                het_index.append(gvariables.DUMMY)
        c_h_chain=len(het_chain);
        if(c_h_chain<nchains):
            #print pdbid,"LESS HET COMPNDS"
            mchain=[];mcompnd=[];mindex=[];
            hcount=0;
            for j in range(nchains):
                nc=het_chain.count(chain_ids[j])
                if(nc==0):
                    mchain.append(chain_ids[j])
                    mcompnd.append("APO")
                    mindex.append(gvariables.DUMMY)
                if(nc==1):
                    mchain.append(het_chain[hcount])
                    mcompnd.append(het_compnd[hcount])
                    mindex.append(het_index[hcount])
                    hcount=hcount+1;
            het_chain=mchain
            het_compnd=mcompnd
            het_index=mindex
        (het_chain,het_compnd,ligdist)=get_pdb_data.process_ligand(organism,sequence,pdb_organism,pdbid,i_pdb,nchains,chain_ids,het_chain,het_compnd,het_index,nchains)
        #print het_chain
        #print het_compnd
        #print ligdist
        lig_dist_data+="%s"%(ligdist)
        if(Calc_Dist==True):
            temp_dist_data=calc_atomic_dist.calculate_distance(organism,sequence,nchains,chain_ids,pdb_organism,pdbid,i_pdb,het_chain,het_compnd)
            for i in range(len(temp_dist_data)):
                id=temp_dist_data[i]
                dist_data+="%s\n"%(id)
                #dist_pdbid.append(id.split()[0])
                fin_dist.append(id)
        if(Calc_Dihedral==True):
            #(temp_dih_data,array_dihed_data)=calc_atomic_dihe.calculate_dihedral(organism,sequence,nchains,chain_ids,pdb_organism,pdbid,i_pdb)
            array_dihed_data=calc_atomic_dihe.calculate_dihedral(organism,sequence,nchains,chain_ids,pdb_organism,pdbid,i_pdb,het_chain,het_compnd)
            for i in range(len(array_dihed_data)):
                fin_dihed.append(array_dihed_data[i])
                dihed_data+="%s\n"%(array_dihed_data[i])
    stats="";
    
    #print fin_dist
    #print dihed_data
    if(Calc_Dist==True):
        #print dist_data
        nclosed_value=10.0;
        cclosed_value=6.50;
        #/////////stats=ana_stats.proc_stats(dist_pdbid,fin_dist,closed_value,fin_dihed,Calc_Dihedral)
        print "Calculating Stats................."
        stats=ana_stats.proc_stats(fin_dist,nclosed_value,cclosed_value,fin_dihed,Calc_Dihedral)
        stats+="\n\nTotal number of chains analyzed: %12d"%(t_n_chains)
        stats+="\nTotal number of PDB's analyzed: %12d"%(num_pdbs)
        print stats
        fName="C:\\Users\\Dhakeneswar\\Desktop\\Papers\\XPAT-DistA.dat"
        w1d.writeData(fName,dist_data)
        fName="C:\\Users\\Dhakeneswar\\Desktop\\Papers\\XPAT-Stats.dat"
        w1d.writeData(fName,stats)
    if(Calc_Dihedral==True):
        #print dihed_data
        fName="C:\\Users\\Dhakeneswar\\Desktop\\Papers\\XPAT-DHA.dat"
        w1d.writeData(fName,dihed_data)

    fName="C:\\Users\\Dhakeneswar\\Desktop\\Papers\\XPAT-LigandAnalysis.dat"
    w1d.writeData(fName,lig_dist_data)
    
    #print lig_dist_data
pdb_files_list="timpdbs.txt";
main(pdb_files_list)
