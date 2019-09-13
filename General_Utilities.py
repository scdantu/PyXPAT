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
#!/usr/bin/python
import os, sys

def check_folder(folder_to_create):
    if(os.path.isdir(folder_to_create)==False):
        mkdir="mkdir %s"%(folder_to_create)
        os.system(mkdir)

def check_file(file_to_check):
    if(os.path.isfile(file_to_check)==False):
        #mkdir="mkdir %s"%(folder_to_create)
        #os.system(mkdir)
        print "Could not find file %s. Exiting"%(file_to_check)
        exit()
