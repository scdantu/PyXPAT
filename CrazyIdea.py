'''
Created on Jan 28, 2012

@author: Dhakeneswar
'''
import numpy
x=[1,2,1,1,1,1,1,2,3,3]
y=[1,2,3,3,1,1,3,2,1,1]

#x=[1,1,1,1,1,1,1,1,1,1]
#y=x;
#y=[1,2,3,3,1,1,3,2,1,1]

(Hx,xH)=numpy.histogram(x,10,[1,10],normed=False)
(Hy,yH)=numpy.histogram(y,10,[1,10],normed=False)
(Hxy,xHy,yHx)=numpy.histogram2d(x, y, 10, [[1,3],[1,3]],normed=False)
print Hx
print Hy
num=len(xH)-1;
n_hxy=[];
oo=0.00;    cc=0.00;
oc=0.00;    co=0.00;
ss=0.00;
data="";
for i in range(num):
    for j in range(num):
        i_j=Hxy[i][j]
        data+="%8.3f"%(i_j)
        #oo
        if(i==0)and(j==0):
            oo=i_j;
        #cc
        if(i==2)and(j==2):
            cc=i_j;
        #ss
        if((i==0)and(j==1))or((i==1)and(j==0))or((i==1)and(j==2))or((i==2)and(j==1)):
            ss=ss+i_j;
        #co
        if(i==0)and(j==2):
            co=i_j;
        #oc
        if(i==2)and(j==0):
            oc=i_j;
    data+="\n"
print data
a=Hx[0]*Hy[0];  b=Hx[1]*Hy[1];  c=Hx[2]*Hy[2]

px_y=[oo,oc,co,ss,cc];
px_py=[a,b,b,b,c]
sum=0.00;
for i in range(len(px_y)):
    nume=px_y[i]*10;    denom=px_py[i];
    if(nume!=0.00)and(denom!=0.00):
        sum=sum+((nume)/denom);
    if(nume==0.00)and(denom==0.00):
        sum=sum+0.00;
    
    #fac=(1.0/5)*sum
print px_y
print px_py
print sum
#print fac