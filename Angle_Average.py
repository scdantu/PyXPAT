'''
Created on Jan 6, 2012

@author: Dhakeneswar
'''
import numpy
import math
def calc_avg(data):
    n_data=len(data)
    avg=0.000;
    sum_sin=0.00;sum_cos=0.000;
    if(n_data>0):
        for i in range(n_data):
            i_d=float(data[i])
            sum_sin=sum_sin+math.sin(i_d)
            sum_cos=sum_cos+math.cos(i_d)
        arctan=0.00;
        #s_by_c=sum_sin/sum_cos
        if(sum_cos>0)and(sum_sin>0):
            arctan=numpy.arctan2(sum_sin,sum_cos)
            #arctan=numpy.arctan(s_by_c)
            avg=numpy.degrees(arctan)
        if(sum_cos<0):
            print "sum_cos>0"
            #arctan=numpy.arctan(s_by_c)
            arctan=numpy.arctan2(sum_sin,sum_cos)
            avg=numpy.degrees(arctan)+180
        if(sum_cos>0)and(sum_sin<0):
            #arctan=numpy.arctan(s_by_c)
            arctan=numpy.arctan2(sum_sin,sum_cos)
            avg=numpy.degrees(arctan)+360
    return avg
def calc_avg2(data):
    n=len(data)
    avg=0.0;std=0.0;sum=0.0;
    for i in range(n):
        i_a=float(data[i])+360
        sum=sum+i_a;
    avg=(sum/n)
    sum=0.0
    for i in range(n):
        i_a=float(data[i])+360
        sum=sum+math.pow(i_a-avg, 2)
    std=math.sqrt(sum/n)
    avg=avg-360
    return std,avg
    
    