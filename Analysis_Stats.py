'''
Created on Jan 2, 2012
@author: Dhakeneswar
'''
import fileIO.Write_1dData as w1d
import Average as avg_py
import numpy
import re as reg_exp
def proc_stats(fin_dist,nclosed_value,cclosed_value,fin_dihed,calc_dihed):
    closed_data="";open_data="";
    closed_data_array=[];open_data_array=[];
    c_data=[];o_data=[];    c_dih=[];o_dih=[];
    n_i=len(fin_dist);    n_j=len(fin_dist);
    not_open_not_closed="";nonc=0;
    if(n_i==n_j):
        for i in range(n_j):
            i_dih="";   nonc=0;
            i_pdbid=fin_dist[i]
            i_pdbid=i_pdbid.split()[0]
            i_dist_data=fin_dist[i];
            i_dist=proc_dist_data(i_dist_data)
            n_dist=i_dist.split()[0]
            n_dist=float(n_dist)
            c_dist=i_dist.split()[1]
            c_dist=float(c_dist)
            if(calc_dihed==True):
                dihed=fin_dihed[i]
                i_dih=proc_dihed_data(dihed)
            if(n_dist<=nclosed_value)and(c_dist<=cclosed_value):
                kdata="%10s%9.3f%9.3f%s"%(i_pdbid,n_dist,c_dist,i_dih)
                closed_data+="%s\n"%(kdata)
                closed_data_array.append(kdata)
                
                c_data.append(i_dist)
                if(calc_dihed==True):
                    c_dih.append(i_dih)
                i_dih=""
                nonc=1;
            if(n_dist>nclosed_value)and(c_dist>cclosed_value):
                kdata="%10s%9.3f%9.3f%s"%(i_pdbid,n_dist,c_dist,i_dih)
                open_data+="%s\n"%(kdata)
                open_data_array.append(kdata)
                o_data.append(i_dist)
                if(calc_dihed==True):
                    o_dih.append(i_dih)
                i_dih=""
                nonc=1;
            if(nonc==0):
                not_open_not_closed+="%10s%9.3f%9.3f%s\n"%(i_pdbid,n_dist,c_dist,i_dih)
        Closed_Mean_Std=[];
        Open_Mean_Std=[];
        #========================================
        stats="*** Closed distance ***\n";
        (istats)=proc_data_stats(c_data)
        stats+="%s\n"%(array_to_string(istats))
        for i in range(len(istats)):
            Closed_Mean_Std.append(istats[i])
        #========================================
        stats+="*** Closed dihedral ***\n";
        (istats)=proc_data_stats(c_dih)
        stats+="%s\n"%(array_to_string(istats))
        for i in range(len(istats)):
            Closed_Mean_Std.append(istats[i])
        #========================================
        stats+="*** Open distance ***\n";
        (istats)=proc_data_stats(o_data)
        stats+="%s\n"%(array_to_string(istats))
        for i in range(len(istats)):
            Open_Mean_Std.append(istats[i])
        #========================================
        stats+="*** Open dihedral ***\n";
        (istats)=proc_data_stats(o_dih)
        stats+="%s\n"%(array_to_string(istats))
        for i in range(len(istats)):
            Open_Mean_Std.append(istats[i])
        #========================================
        #print stats
        fName="C:\\Users\\Dhakeneswar\\Desktop\\Papers\\XPAT-Open.dat"
        w1d.writeData(fName,open_data)
        fName="C:\\Users\\Dhakeneswar\\Desktop\\Papers\\XPAT-Closed.dat"
        w1d.writeData(fName,closed_data)
        closed_anamolies=pick_anamolies(closed_data_array,Closed_Mean_Std)
        open_anamolies=pick_anamolies(open_data_array,Open_Mean_Std)
        anamolies="*** CLOSED STATE ANOMALIES\n"
        anamolies+="%s\n"%(closed_anamolies)
        anamolies+="*** OPEN STATE ANOMALIES\n"
        anamolies+="%s\n"%(open_anamolies)
        anamolies+="*** Not Open Not Closed\n"
        anamolies+="%s\n"%(not_open_not_closed)
        fName="C:\\Users\\Dhakeneswar\\Desktop\\Papers\\XPAT-Anamolies.dat"
        w1d.writeData(fName,anamolies)
        (closed_apo,closed_holo)=proc_apo_holo(closed_data_array)
        (open_apo,open_holo)=proc_apo_holo(open_data_array)
        apo_holo_stats="==== APO & HOLO stats ====\n"
        apo_holo_stats+="%12s%12s%12s\n"%("STATE","APO","HOLO");
        apo_holo_stats+="%12s%12d%12d\n"%("Open",open_apo,open_holo);
        apo_holo_stats+="%12s%12d%12d\n"%("Closed",closed_apo,closed_holo);
        stats+="\n%s"%(apo_holo_stats)
        #print stats
        #print anamolies
    return stats
def proc_apo_holo(data):
    apo_count=0;    holo_count=0;
    len_data=len(data);
    for i in range(len_data):
        i_str=data[i]
        i_str=i_str.split()
        istr=i_str[0]
        i_str=reg_exp.split('-',istr)
        #print i_str
        i_state=i_str[2]
        
        if(i_state=="APO"):
            apo_count=apo_count+1;
        if(i_state!="APO"):
            holo_count=holo_count+1;
    return apo_count,holo_count

def pick_anamolies(data,mean_std):
    anamolie_stats="*** NO ANOMALIES ***";title="";
    title_array=["A-dist","B-dist","220-Phi","220-Psi",
                                  "221-Phi","221-Psi",
                                  "222-Phi","222-Psi",
                                  "223-Phi","223-Psi",
                                  "224-Phi","224-Psi",
                                  "225-Phi","225-Psi"];
    temp_str=data[0];   tstr=temp_str.split();
    num_dih=len(tstr);len_data=len(data);
    count=0;
    for i in range(len_data):
        t_data=[];
        i_dih=data[i]
        i_dih=i_dih.split()
        for j in range(1,num_dih):
            idih=float(i_dih[j])
            t_data.append(idih)
        #using len(t_data)-1 since we dont want to analyze the
        #N214-Psi since it has some problems with periodicity
        for k in range(len(t_data)-1):
            ist=mean_std[k]
            ist=ist.split()
            imean=float(ist[0])
            istd=(float(ist[1])*3)
            if(k>=2):
                istd=25.00;
            ul=imean+istd;ll=imean-istd;
            ith_value=t_data[k]
            if(ith_value>ul)or(ith_value<ll):
                if(count==0):
                    title="%10s"%("Avg");
                    ori_stats="%10s"%("Avg");
                    for n in range(len(mean_std)):
                        ist=mean_std[n]
                        ist=ist.split()
                        imean=float(ist[0])
                        ori_stats+="%9.3f"%(imean)
                        title+="%9s"%(title_array[n])
                    anamolie_stats="%s\n"%(title)
                    anamolie_stats+="%s\n"%(ori_stats)
                    anamolie_stats+="%s%3d\n"%(data[i],k+1);
                if(count>0):
                    anamolie_stats+="%s%3d\n"%(data[i],k+1);
                count=count+1;
                break;
    return anamolie_stats

def proc_data_stats(c_data):
    dih_stats=[];   temp_data=[];   limit=25.00;
    len_c_data=len(c_data);
    temp_str=c_data[0];
    temp_str=temp_str.split();
    num_dih=len(temp_str);
    for i in range(num_dih):
        temp_data=[];
        for j in range(len_c_data):
            i_dih=c_data[j]
            #print i_dih
            i_dih=i_dih.split()
            i_dih=float(i_dih[i])
            temp_data.append(i_dih)
        (mean,std)=calc_stats(temp_data)
        mean=float(mean);        std=float(std);

        if(std<=limit):
            limit=std*3;
        if(std>limit):
            limit=limit;

        new_data=[];
        for k in range(len(temp_data)):
            ul=mean+limit;ll=mean-limit;
            ith=float(temp_data[k])
            if(ith>=ll)and(ith<=ul):
                new_data.append(ith)
        (mean,std)=calc_stats(new_data)
        mean=float(mean);        std=float(std);
        stats="%9.3f%9.3f"%(mean,std);
        dih_stats.append(stats)
    return dih_stats
def calc_stats(array):
    mean=0.0;std=0.0;
    mean=avg_py.calc_avg(array)
    std=numpy.std(array)
    return mean,std
def proc_dist_data(dist):
    split_str=dist.split()
    len_d=len(split_str)
    i_str="";
    for i in range(len_d):
        if(i>0):
            i_d=float(split_str[i])
            i_str+="%9.3f"%(i_d)
    return i_str
def proc_dihed_data(dihed):
    split_str=dihed.split()
    len_d=len(split_str)
    i_str="";
    for i in range(len_d):
        if(i>0):
            i_d=float(split_str[i])
            i_str+="%9.3f"%(i_d)
    return i_str
def array_to_string(istats):
    string_stats="";
    for i in range(len(istats)):
        string_stats+="%s\n"%(istats[i])
    return string_stats