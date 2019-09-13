'''
Created on Dec 27, 2011

@author: Dhakeneswar
'''
import numpy as nump
import math
import Global_Variables as gvariables
#def CalcDihedralAngle(x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4):
def CalcDihedralAngle(vector):
    x1=float(vector[0][0]);y1=float(vector[0][1]);z1=float(vector[0][2]);
    x2=float(vector[1][0]);y2=float(vector[1][1]);z2=float(vector[1][2]);
    x3=float(vector[2][0]);y3=float(vector[2][1]);z3=float(vector[2][2]);
    x4=float(vector[3][0]);y4=float(vector[3][1]);z4=float(vector[3][2]);
    numerator=0.0;  denominator=0.0;    acos=0.0;
    n1Len=0.0;      n2Len=0.0;          vecdot=0.0;
    n3X=0.0;        n3Y=0.0;            n3Z=0.0;
    a12X=0.0;       a12Y=0.0;           a12Z=0.0;
    a23X=0.0;       a23Y=0.0;           a23Z=0.0;
    a34X=0.0;       a34Y=0.0;           a34Z=0.0;
    n1X=0.0;        n1Y=0.0;            n1Z=0.0;
    n2X=0.0;        n2Y=0.0;            n2Z=0.0;
    sign=0.0;
    #final result
    dihedralAngle=0.0;
    '''
        /**
         *    To calculate diheral angles from 4, 3D vectors a1,a2,a3,a4 the formula is
         *    theta in radians=(n1.n2)/|n1|*|n2|
         *    theta in degrees= theta in radians*180/pi
         *    Where n1 and n2 are normal vectors of a1-a2-a3 and a2-a3-a4 respectively 
         *    ******* How to determine the sign since acos gives values only between 0-180 *******      
         *    
         *              
         * 
         **/
    '''
    #a1 a2 a3 a4 are the 4 vectors 
    #a12=a2-a1            a23=a3-a2        a34=a4-a3
    #a12=a2-a1
    a12X=(x2-x1);            a12Y=(y2-y1);            a12Z=(z2-z1);
    #a23=a3-a2
    a23X=(x3-x2);            a23Y=(y3-y2);            a23Z=(z3-z2);
    #a34=a4-a3
    a34X=(x4-x3);            a34Y=(y4-y3);            a34Z=(z4-z3);
    #n1=a12 X a23
    n1X=(a12Y*a23Z)-(a12Z*a23Y);            n1Y=(a12X*a23Z)-(a12Z*a23X);            n1Z=(a12X*a23Y)-(a12Y*a23X);
    #n2=a23 X a34
    n2X=(a23Y*a34Z)-(a23Z*a34Y);            n2Y=(a23X*a34Z)-(a23Z*a34X);            n2Z=(a23X*a34Y)-(a23Y*a34X);
    #length of a12Xv23
    n1Len=nump.sqrt((n1X*n1X)+(n1Y*n1Y)+(n1Z*n1Z));
    #length of n2
    n2Len=nump.sqrt((n2X*n2X)+(n2Y*n2Y)+(n2Z*n2Z));
    #normalizing v2Xv1
    numerator=(n1X*n2X)+(n1Y*n2Y)+(n1Z*n2Z);            denominator=n1Len*n2Len;
    #print numerator,denominator
    if(numerator!=0)and(denominator!=0):
        vecdot=numerator/(denominator);
        #print vecdot
        #n3=n1Xn2
        n3X=(n1Y*n2Z)-(n1Z*n2Y);            n3Y=(n1X*n2Z)-(n1Z*n2X);            n3Z=(n1X*n2Y)-(n1Y*n2X);
        sign=(n3X*a23X)+(n3Y*a23Y)+(n3Z*a23Z);
        acos=nump.arccos(vecdot);            
        dihedralAngle=math.degrees(acos)
        pi=3.14159265
        #print math.pi
        rad_2_deg=(acos*180.00)/pi
        #print "%8.3f%8.3f%8.3f%8.3f"%(vecdot,acos,dihedralAngle,rad_2_deg)
        if(sign>0):
            dihedralAngle=0-dihedralAngle;
        if(sign==0):
            dihedralAngle=180.00;
    if(numerator==0)or(denominator==0):
            dihedralAngle=(gvariables.DUMMY)/1000
    return dihedralAngle;