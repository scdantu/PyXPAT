#!/usr/bin/python
'''
    @release_date  : $release_date
    @version       : $release_version
    @author        : Sarath Chandra Dantu
    

     Copyright (C) 2011-2019 Sarath Chandra Dantu 

     This file is part of: XPAT

     XPAT is a free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     XPAT is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with XPAT.  If not, see <http://www.gnu.org/licenses/>.

'''
import Global_Variables as gv
def get_resolution(fOpen):
    resolution=gv.DUMMY;
    fileOpen=open(fOpen,"r")
    for line in fileOpen:
        split_line=line.split()
        if(len(split_line)==5):
            #print split_line
            if(split_line[0]=="REMARK")and(split_line[1]=="2")and(split_line[2]=="RESOLUTION."):
                resolution=float(split_line[3])
                break
    return resolution
def get_num_chains(fOpen):
    num_chains=gv.DUMMY;
    chain_ids=[]
    fileOpen=open(fOpen,"r")
    for line in fileOpen:
        split_line=line.split()
        if(len(split_line)==5):
            #print split_line
            if(split_line[0]=="REMARK")and(split_line[1]=="2")and(split_line[2]=="RESOLUTION."):
                num_chains=float(split_line[3])
                break
    return num_chains,chain_ids

