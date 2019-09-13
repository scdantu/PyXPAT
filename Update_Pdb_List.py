'''
Created on Dec 7, 2011

@author: Dhakeneswar
'''
def update_pdb_list(oldlist,remove_item):
    count=oldlist.count(remove_item)
    for i in range(count):
        oldlist.remove(remove_item)
    return oldlist
