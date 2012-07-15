#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from __future__ import division
import os,glob
import commands
import time
import datetime
import shutil
from gps.config import CONFIG
from gps.utils import dToMd,isLeap


#cwd=os.path.dirname(__file__)
cwd=CONFIG.SOFTWAREPATH

#typename指的是从批量常规处理中得到的数据还是从大气天顶延迟中得到的数据 typename = [batch, atmosphere]
#基线处理和大气处理记录某些本地站（可选）的某段时间内的大气天顶延迟数据
#批量常规处理记录所有本地站的所有时间内的大气天顶延迟数据

def getData(typename,user):                             #extract data into file
    
    atmosphere_path=''
    if typename == 'atmosphere':
        atmosphere_path=os.path.join(cwd,user,'exp2nd/atmosphere')
        filepath = os.path.join(atmosphere_path,'atmosphere.dat')
        if os.path.isfile(filepath) == True:
            os.remove(filepath)
    elif typename == 'batch':
        atmosphere_path=os.path.join(cwd,user,'exp2nd/atmosphere_batch')
    
    
    oscala_path=os.path.join(cwd,user,'exp2nd/oscala_%s/oscala.*' % typename)
    

    list_files = os.popen("dir %s" % oscala_path).read().split() #按生成创建时间排列文件
    list_files.sort()

    for l in list_files:
        (oscala_path,filename)=os.path.split(l)
        year_day=filename.split('.')
        year=year_day[1]
        day=year_day[2]
        

        d = dToMd(year,day)
        format='"%.6f ",'
        sum_day=isLeap(int(year))
        hour_base = sum_day*24
        
        cmd=" awk '/^ATM/ && $2~/X/ && /[0-9]$/ {if($7==%d) {printf(%s$5+%f/%d+$8/%d);print $3,$12,$13}}' %s >> %s/atmosphere.dat " % (d,format,float(day),sum_day,float(hour_base),l,atmosphere_path)
            
        print cmd
     
        os.popen(cmd)    
        
       
if __name__ == '__main__':
    #getData('atmosphere')
    getData('batch')
