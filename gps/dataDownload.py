#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import shutil
import time 
import datetime
from subprocess import *
from gps.utils import ymdToYd
from gps.config import CONFIG
#cwd=os.path.dirname(__file__)
cwd=CONFIG.SOFTWAREPATH

def deleteFile(filetype):
    
    filepath = cwd+'/data_download/'+ "%s" % filetype
    
    if os.path.isdir(filepath) == True:
        m = time.localtime(os.stat(filepath).st_ctime) 
        starttime = datetime.datetime(m.tm_year,m.tm_mon,m.tm_mday,m.tm_hour,m.tm_min,m.tm_sec)
        endtime = datetime.datetime.now()
        
        intervel = (endtime-starttime).days
        if intervel>30:
            shutil.rmtree(filepath)
            print 'delete!'
        else:
            print 'less than 30 days!'

def downloadOfile(timelist,siteslist):
    filedir = os.path.join(cwd,'data_download/o_files')
    
    if os.path.isdir(filedir) == True:
        deleteFile('o_files')
    else :
        os.mkdir(filedir)
        print 'new file'
    
    for t in timelist:    
        cmd = "cd %s;sh_get_rinex -archive cddis  -yr %s -doy %s -ndays %s -sites %s" % (filedir,t[0],t[1],t[2],siteslist)
        print cmd
        call(cmd,shell=True)
    

def downloadNfile(timelist):
    filedir = os.path.join(cwd,'data_download/n_files')
    
    if os.path.isdir(filedir) == True:
        deleteFile('n_files')
    else:
        os.mkdir(filedir)
        print 'new dir'
    
    for t in timelist:
        cmd = "cd %s;sh_get_nav -archive cddis -yr %s -doy %s -ndays %s" % (filedir,t[0],t[1],t[2])
        print cmd
        call(cmd,shell=True)
    

def downloadSp3file(timelist):
    filedir = os.path.join(cwd,'data_download/sp3_files')
    
    if os.path.isdir(filedir) == True:
        deleteFile('sp3_files')
    else:
        os.mkdir(filedir)
        print 'new dir'
    
    for t in timelist:   
        cmd = "cd %s;csh %s/get_orbits -archive cddis -yr %s -doy %s -ndays %s" % (filedir,cwd,t[0],t[1],t[2])
        print cmd
        call(cmd,shell=True)

def isLeap(year):
    if (year%4==0 and year%100!=0) or (year%100==0 and year%400==0):
        return 366
    else:
        return 365 

#以上三个命令不能跨年下载数据
def intervel(start_year,start_month,start_day,end_year,end_month,end_day):
    start_y = int(start_year)
    start_m = int(start_month)
    start_d = int(start_day)
    end_y = int(end_year)
    end_m = int(end_month)
    end_d = int(end_day)   
    startdays=ymdToYd(start_y,start_m,start_d) 
    enddays=ymdToYd(end_y,end_m,end_d)
    
    intervel = 0
    timelist = []
    
    if start_y == end_y:
        intervel = enddays - startdays + 1
        timelist.append([start_year,str(startdays),str(intervel)]) 
    
    if start_y < end_y:
        start = 0
        for y in range(start_y,end_y+1):
            if(y==start_y):
                start = startdays
                intervel = isLeap(y)-startdays+1
            elif(y==end_y): 
                start = 1 
                intervel = enddays
            else:
                start = 1
                intervel = isLeap(y)
            timelist.append([str(y),str(start),str(intervel)])
    
    print timelist
    return timelist

def zipData(data_type):
    
    orgFile=''
    if data_type=='o':    
        orgFile = 'o_files'
    elif data_type=='n':
        orgFile ='n_files'
    elif data_type=='s':
        orgFile = 'sp3_files'
    zipFile = os.path.join(cwd,'data_download')
    os.popen('cd %s ; zip -r %s.zip %s' % (zipFile,orgFile,orgFile))
    
if __name__ == '__main__':
    timelist=intervel('2008', '9', '1', '2008', '9', '2')
    downloadSp3file(timelist)
    #downloadNfile(timelist)
    #downloadNfile('2000','123','1')
    #downloadSp3file('2001','122','2')
    #downloadOfile(timelist,'algo drao ankr')
