'''
Created on Dec 2, 2011

@author: Dhakeneswar
'''
from optparse import OptionParser 

def parseOptions():
    parser = OptionParser()
    parser.add_option("-c", "--cluw", dest="cluw", help="ClustalW file")
    parser.add_option("-m", "--meta", dest="meta", help="PDB file list")
    parser.add_option("-o", "--out", dest="out", help="Out File")
    parser.add_option("-g", "--log", dest="log",default="1", help="1 for log file writing, 0 for quite")
    parser.add_option("-d", "--dist", dest="dist",default="7", help="7 for S212, 8 for V232")
    (options, args) = parser.parse_args()
    if((options.cluw==None))and(options.meta==None):
        print "************************ERROR ERROR ERROR ERROR **********************************"
        print
        print "No file specified with -f or -m. Specify either a single file or a metadata file."
        print "With -f option use -l and specify out label"
        print
        print "************************ERROR ERROR ERROR ERROR **********************************"
        exit(1)
    elif (options.dist==None):
        print "************************ERROR ERROR ERROR ERROR **********************************"
        print
        print "Please specify if you want to use S212 (7) as ref or V232 (8) as ref."
        print
        print "************************ERROR ERROR ERROR ERROR **********************************"
        exit(1)
    elif ((options.file1!=None)and(options.label==None)):
        print "************************ERROR ERROR ERROR ERROR **********************************"
        print
        print "With -f option use -l and specify out label"
        print
        print "************************ERROR ERROR ERROR ERROR **********************************"
        exit(1)
    return options

def umb_parseOptions():
    parser = OptionParser()
    parser.add_option("-m", "--meta", dest="meta", help="Metadata file")
    parser.add_option("--minv","--minv", dest="minv",default=0,help="min along the vector")
    parser.add_option("--maxv","--maxv", dest="maxv",default=0,help="max along the vector")
    parser.add_option("--dv","--dvec", dest="dvec",default=0,help="distance between neighbouring umbrella windows")
    (options, args) = parser.parse_args()
    if((options.minv==0))and(options.maxv==0):
        print "************************ERROR ERROR ERROR ERROR **********************************"
        print
        print "Please specify limits for the vector."
        print "--minv -2 --maxv 2"
        print
        print "************************ERROR ERROR ERROR ERROR **********************************"
        exit(1)
    elif (options.dvec==0):
        print "************************ERROR ERROR ERROR ERROR **********************************"
        print
        print "Please specify the dvec. It cant be zero"
        print
        print "************************ERROR ERROR ERROR ERROR **********************************"
        exit(1)
    elif (options.meta==None):
        print "************************ERROR ERROR ERROR ERROR **********************************"
        print
        print "Please specify a metadata file"
        print
        print "************************ERROR ERROR ERROR ERROR **********************************"
        exit(1)
    return options
