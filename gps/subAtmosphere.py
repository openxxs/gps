#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division
import os,glob
import commands
import shutil
from gps.config import CONFIG

start_string = 'ATM_ZEN'  
    
def extractData(user):   
    
    filedir1=os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd')
    #if os.path.isdir("%s/oscala_result" % filedir1) != True: 
        #没有生成oscala_result文件夹说明上一步extractFile操作没有完成应该提示用户无
        #文件可显示，请联系管理员重新生成
        #os.mkdir("%s/oscala_result" % filedir1)
    filedir2 = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/oscala_result')  #new file
    filedir3 = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/sub_atmosphere')
        
    #每次生成文件时删除上次生成的文件
    if os.path.isdir("%s/temp" % filedir3) == True:  
        shutil.rmtree("%s/temp" % filedir3)
    os.mkdir("%s/temp" % filedir3)  
   
    #暂时假定在数据处理时确定的时间间隔之内选择结果精度时间段
    year_3 = '2000'
    day_3 = '365'
    year_4 = '2001'
    day_4 = '004'
    start_year = int(year_3)
    end_year = int(year_4)
    start=int(day_3)
    end = int(day_4)
    
    fileList=[]
    
    if start_year == end_year:
               
        for d in range(start,end+1):
            d_str = numberToDay(d)
            filename = 'oscala.'+str(start_year)+'.'+d_str
            fileList.append(filename)
   
    if  start_year <  end_year:
        for y in range(start_year,end_year+1):
            if(y==start_year):
                start=int(day_3)
                end = isLeap(y)
            elif(y==end_year):  
                start=1
                end = int(day_4)
            else:
                start=1
                end = isLeap(y)
            for d in range(start,end+1):
                d_str = numberToDay(d)
                filename = 'oscala.'+str(y)+'.'+d_str
                fileList.append(filename)
    
    for l in fileList:
        
        filepath = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/oscala_result/%s' % l)
        
        if os.path.isfile(filepath) == True :
            
            temp=l.split('.')
            
            day=(int)(temp[2])
            year=(int)(temp[1])
            sum_day = isLeap(year) 
        
            if(day == sum_day):
                time_ratio = 0.0000 + year
            else:
                time_ratio = day/sum_day + year
        
            format='"%.4f ",'+str(time_ratio)           
            lastCol = '0.0000'   #大气延迟最后一行误差全部显示为0
            
            cmd = " awk '/^%s/&&/[0-9]$/{printf(%s);print $13,%s}' %s >> %s/temp/data.txt " % (start_string,format,lastCol,filepath,filedir3) 
                  
            os.popen(cmd)

def createImage(user):
    path = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/sub_atmosphere/temp')
    filename =  os.path.join(path,"data.txt")
    #如果没有数据文件则不生成图片
    if os.path.isfile(filename) == True:
        imagename = os.path.join(path,'image.pdf')
        commands.getstatusoutput('psxy %s -JX6.5/2.0 -R2002.8/2004.5/-70/64 -Ba0.5f0.1:"":/a20f5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i > %s' % (filename,imagename))   
     
if __name__ == '__main__':
    extractData()
    createImage()
