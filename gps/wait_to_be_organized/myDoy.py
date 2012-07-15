#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os

def mon2day(year,month):
    unleap = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    if(isLeap(year)==366 and month==2):
        return 29    
    else:
        return unleap[month]
            
def doy(date):#这一块需要将输入的数据放到一个数组里，比如输入为年月日，则date大小为三，输入为年日，date大小为二

    if len(date)==3:      
        if(int(date[1])>12):
            date[1]='12'
        elif(int(date[1])<1):
            date[1]='1'        
        os.popen("doy %s %s %s | awk 'NR==1{print $2,$6,$10}NR==2{Decimal = $3+''+$7;print Decimal}NR==3{print $3}' >tmp" % (date[0],date[1],date[2])) 
                                 
    if len(date)==2:             
        os.popen("doy %s %s | awk 'NR==1{print $2,$6,$10}NR==2{Decimal = $3+''+$7;print Decimal}NR==3{print $3}' >tmp" % (date[0],date[1])) 
    f = open("tmp","r")
    doyResult=[]   
    for line in f:
        doyResult.append(line)
    os.popen('rm tmp')
    print doyResult
    return doyResult   
       
if __name__ == '__main__':
    date=["2003","2","30"]
    doy(date)

