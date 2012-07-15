#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import extractOscalaFile

def ymdToYd(year,month,day):
    y = int(year)
    m = int(month)
    d = int(day)
    unleap = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    leap = [0,31,29,31,30,31,30,31,31,30,31,30,31]
    
    sum_day = 0
    i = 1
    if extractOscalaFile.isLeap(y) == 366:
        while(i<m):
            sum_day += leap[i]
            i += 1
    
    else:
        while(i<m):
            sum_day += unleap[i]
            i += 1
            
    sum_day += d
    return sum_day
    
#if __name__ == '__main__':
    #print ymdToYd('2000','3','3')
    #print ymdToYd('2001','3','3')
    
