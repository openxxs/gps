#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import extractOscalaFile

def dToMd(year,days):
    y = int(year)
    ds = int(days)
    unleap = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    leap = [0,31,29,31,30,31,30,31,31,30,31,30,31]
    
    m = 1
    d = ds
    i = 1
    if extractOscalaFile.isLeap(y) == 366:

        while (d>leap[i]):
            d -= leap[i]
            m +=1
            i +=1 
    else:
        while (d>unleap[i]):
            d -= unleap[i]
            m +=1
            i +=1 
        
    return d#((y,ds),(y,m,d))
    
if __name__ == '__main__':
    print dToMd('2001','001')
    print dToMd('2000','366')    
