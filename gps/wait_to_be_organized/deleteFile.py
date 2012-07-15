#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import time
import datetime

#定时删除文件

def checktime(p):
    pathlist = os.listdir(p)
    extlist = ['csv','sum','out','LC','status','fatal','warning']
    
    for i in range(len(pathlist)):
    
        source=p+'/'+pathlist[i]
        print source
        
        if os.path.isfile(source):
            m=time.localtime(os.stat(source).st_ctime) #文件创建时间
            
            starttime = datetime.datetime.now() #当前时间
            endtime = datetime.datetime(m.tm_year,m.tm_mon,m.tm_mday,m.tm_hour,m.tm_min,m.tm_sec)
            
            mydays=(starttime-endtime).days  #计算时间间隔
            #print mydays
            ext=source.split('.')[-1]  #文件后缀名
            
            print ext
            
            if mydays>=1 and ext in extlist:
                #一天清空一次
                os.remove(source)
                print 'delete',source
                
if __name__ == '__main__':
    try:
        checktime('/home/bxy/trunk/Amchat1/demo')  
    except Exception:
        print 'error'                 
