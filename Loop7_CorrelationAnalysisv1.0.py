'''
Created on Jan 6, 2012
@author: Dhakeneswar
'''
#!/usr/bin/python
import numpy
import fileIO.Write_1dData as w1dData
import scipy.stats as stats
import pdbAnalysis.NormalityTest as ntest
progname="Loop6_CorrelationAnalysis.py";version=" v1.0"
corr_coef="%12s%12s%12s%12s\n"%("Label","r","r^2","p")
dummy=999999;aSize=100000;
ang_data=[[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize]
#psi_data=[[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize]
nspear=0;npearson=0;len_data=0;
time=[];icount=0;
size=10;
m_avg_corr="";
zmat=[[dummy]*size,[dummy]*size,[dummy]*size,[dummy]*size,[dummy]*size,
      [dummy]*size,[dummy]*size,[dummy]*size,[dummy]*size,[dummy]*size]
title_array=["Angle","210-Phi","210-Psi",
            "211-Phi","211-Psi",
            "212-Phi","212-Psi",
            "213-Phi","213-Psi",
            "214-Phi","214-Psi",
            "215-Phi","215-Psi"];
l7_open=[-89.615,125.777,-111.668,23.526,-89.517,-162.155,
         -69.599,114.566,-124.916,132.566,-133.683,173.671]
l7_closed=[-103.145,139.845,-139.330,152.321,126.675,93.140,
           63.484,32.000,-73.009,133.152,-136.460,173.033]
def parseMetaFile(metaFile,olabel):
    global nspear,npearson
    global time,ang_data,icount,m_avg_corr
    fileOpen = open (metaFile,"r")
    inFile=[];    oFile=[];
    for line in fileOpen:
        inFile.append(line.split()[0])
        oFile.append(line.split()[1])
    print "Found %d files " %(len(inFile))
    corr_Data="";ifilecount=0;
    for i in range(len(inFile)):
        if(inFile[i]!="ENDOFFILE"):
            print "processing file %s"%(inFile[i])
            readList(inFile[i],oFile[i])
            icount=icount+2
        if(inFile[i]=="ENDOFFILE"):
            sOpen=oFile[i-1]
            icount=0;
            corr_Data+=calc_corr(sOpen)
            ang_data=[[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize,[dummy]*aSize]
            ifilecount=ifilecount+1;
    m_avg_corr+="******************************************\n"
    m_avg_corr+="*** File: %20s\n"%(olabel)
    global title_array
    zout="*** Average Correlation Coefficients ***\n"
    for i in range(11):
        zout+="%8s"%(title_array[i])
    zout+="\n"
    for i in range(10):
        zout+="%8s"%(title_array[i+1])
        for j in range(10):
            i_j=zmat[i][j]
            div=i_j/float(ifilecount);
            zmat[i][j]=z_to_r(div)
            zout+="%8.3f"%(zmat[i][j])
        zout+="\n"
    m_avg_corr+="%s"%(zout)

    corr_Data+="\n\n%s"%(zout)
    ofile="C:\Users\Dhakeneswar\Desktop\%s-L7-N_C-ter-Correlation.dat"%(olabel)
    w1dData.writeData(ofile,corr_Data)

def z_to_r(z):
    exp_2=numpy.exp(z*2)
    r=(exp_2-1)/(exp_2+1);
    return r

def calc_corr(sOpen):
    global ang_data,len_data
    global dummy,zmat
    corr_coef="%12s\n"%(sOpen);
    corr_coef+="%s\n"%("--------------------------------------------------------");
    ndata=len(ang_data[0]);
    a=ang_data[0];
    count=a.count(dummy);
    xdata=ndata-count;
    print len(ang_data),len(time),len(ang_data),len(ang_data[0]),xdata
    a=[];b=[];
    for i in range(11):
        corr_coef+="%8s"%(title_array[i])
    corr_coef+="\n"
    for i in range(10):
        #if(i>0):
        corr_coef+="%8s"%(title_array[i+1])
        for j in range(10):
            a=[];b=[];
            for k in range(xdata):
                a.append(ang_data[i][k])
                b.append(ang_data[j][k])
            (coef,p)=stats.spearmanr(a,b,axis=0)
            corr_coef+="%8.3f"%(coef)
            old_z=zmat[i][j]
            c_z=calc_z(coef)
            iz=0;
            if(old_z!=dummy):
                iz=old_z+c_z;
            if(old_z==dummy):
                iz=c_z;
            zmat[i][j]=iz
        corr_coef+="\n"
    return corr_coef


def calc_z(coef):
    z=0.0;
    num=(1+coef);
    denom=(1-coef);
    #print num,denom
    if(denom!=0)and(num!=0):
        div=num/float(denom)
        z=0.5*numpy.log(div)
    return z

def readList(aOpen,sOpen):
    global corr_coef,npearson,nspear
    global ang_data,time,icount,len_data
    ph_data=[];        ps_data=[]
    time=[]; 
    fileOpen = open (aOpen,"r")
    for line in fileOpen:
        ph_data.append(float(line.split()[0]))
        ps_data.append(float(line.split()[1]))
        time.append(float(line.split()[2]))
    ndata=len(ph_data)
    i_t=0;
    for i in range(ndata):
        #i_t=(time[i]*2000)
        if((i_t==0)):
            ang_data[icount][i]=ph_data[i]
            ang_data[icount+1][i]=ps_data[i]
            i_t=0;
        i_t=i_t+0;

def main():
    global logging,version, progname
    global m_avg_corr
    '''
    options = parse_options.parseOptions()
    dataFile=options.file1
    metaFile=options.meta
    label=options.label
    if((options.file1 != None)and(options.label != None)):
        #options.meta=None
        print "Processing the Single file %s"%(dataFile)
        parseSingleFile(dataFile,label)
    elif (options.meta != None):
        options.file1=None
        print "Processing the Metadata file %s"%(metaFile)
    '''
    m_avg_corr="==== Average Correlation Coefficients of All files ===\n"
    super_metaFile="C:\\Users\Dhakeneswar\\Desktop\\l7_correlation\\L7-Correlation.dat"
    fileOpen = open (super_metaFile,"r")
    for line in fileOpen:
        metaFile=line.split()[0]
        olabel=line.split()[1]
        parseMetaFile(metaFile,olabel)    
    fname="C:\\Users\Dhakeneswar\\Desktop\\l7_correlation\\Global-L7-Correlation.dat"
    w1dData.writeData(fname,m_avg_corr)
    print "processing of all files Done..hahahah"

main()