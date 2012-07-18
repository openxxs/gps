#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os,glob
import commands
import monthToDay
import shutil
from gps.config import CONFIG
from gps.utils import isLeap


start=''
end=''
syear=0
eyear=0
sday=0
eday=0

state=''
time=''

from gps.config import CONFIG

def getState(s):  #获取台站
    global state 
    state = s.upper()

def getTimeSlot(start_y,start_m,start_d,end_y,end_m,end_d,now):  #获取时间段
    global sday,eday,syear,eyear,time
    syear=int(start_y)
    sm=int(start_m)
    sd=int(start_d)
    eyear=int(end_y)
    em=int(end_m)
    ed=int(end_d)
    sday = monthToDay.ymdToYd(syear,sm,sd)
    eday = monthToDay.ymdToYd(eyear,em,ed)
    time=now

def changeToFraction(y,d):
    sum_day = isLeap(y)
    sum_time = y+float(d)/sum_day
    s_time = '%.5f' % sum_time
    #print s_time
    return s_time 
    
def getData(user):   
    filedir1=os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd')
    filedir3 = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/TimeSeries_accuracy')
   
    stime = changeToFraction(syear,sday)
    etime = changeToFraction(eyear,eday+1)
                
    #每次生成临时文件
    if os.path.isdir("%s/temp" % filedir3) == True:  
        shutil.rmtree("%s/temp" % filedir3)
    os.mkdir("%s/temp" % filedir3)
    
    cmd1 ="awk '{if($1>=%s && $1<%s) print $1,$2,0}' %s/%s > %s/temp/timeSeriesAccuracy%s.N" % (stime, etime, filedir3, state, filedir3,time)
    os.popen(cmd1)
    cmd2 ="awk '{if($1>=%s && $1<%s) print $1,$4,0}' %s/%s > %s/temp/timeSeriesAccuracy%s.U" % (stime, etime, filedir3, state, filedir3,time)
    os.popen(cmd2)
    cmd3 ="awk '{if($1>=%s && $1<%s) print $1,$5,0}' %s/%s > %s/temp/timeSeriesAccuracy%s.E" % (stime, etime, filedir3, state, filedir3,time)
    os.popen(cmd3)
        
def createImage(user):
    startTime = syear
    endTime = eyear+1
    postfix = ['N','E','U']
    path = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/TimeSeries_accuracy/temp')
    for p in postfix:
        filename =  os.path.join(path,'timeSeriesAccuracy'+time+'.%s' % p)
        #如果没有数据文件则不生成图片
        if os.path.isfile(filename) == True:
            imagename = filename+".pdf"
            commands.getstatusoutput('psxy %s -JX6.5/2.0 -R%d/%d/-10/10 -Ba0.5f0.1:"":/a10f5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i > %s' % (filename,startTime,endTime,imagename))    
            os.popen('convert -trim %s %s' %(imagename,filename+'.png')) 

def timeSeriesAccuracy(s,s_y,s_m,s_d,e_y,e_m,e_d,now,user):
    getState(s)
    getTimeSlot(s_y,s_m,s_d,e_y,e_m,e_d,now)
    getData(user)
    createImage()
    
if __name__ == '__main__':
    timeSeriesAccuracy('jplm','2009','12','31','2010','1','2','')
