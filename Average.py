#!/usr/bin/python
'''
Created on Nov 18, 2011

@author: dsarath
'''
import numpy
import NormalityTest as ntest
def calc_avg(a):
    avg=0.0;
    if(len(a)>0):
        isNormal=ntest.do_kstest(a)
        #print isNormal
        if(isNormal==False):
            avg=numpy.median(a)
        elif(isNormal==True):
            avg=numpy.average(a)
    return avg
