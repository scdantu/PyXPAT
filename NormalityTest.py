#!/usr/bin/python
'''
Created on Nov 18, 2011

@author: dsarath
'''
import numpy
import scipy.stats as stats
def do_kstest(a):
    isNormal=True
    if(len(a)>0):
        avg=numpy.average(a)
        std=numpy.std(a)
        normed_data=(a-avg)/std
        k,p=stats.kstest(normed_data,'norm')
        if(p<0.05):
            isNormal=False
    return isNormal