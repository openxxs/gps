#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division
import os,glob
import commands
import time
import datetime
import extractOscalaFile
import shutil
from gps.config import CONFIG
#基线处理中提取oscala文件需要实现两个功能：1.令用户选择从上次更新后的时间开始提取数据；2.允许用户重新生成所有的oscala文件（即删除现有的重新生成一遍）

#cwd+user = os.path.dirname(__file__)
cwd= CONFIG.SOFTWAREPATH

from gps.utils import numberToDay,isLeap

# typename baseline atmosphere 不需要时间记录  创建临时文件夹 oscala_baseline oscala_atmosphere      
def extractTempFile(start_year,start_day,end_year,end_day,typename,user): 
        
    filedir1=os.path.join(cwd+user,'exp2nd')
    filedir2=os.path.join(cwd+user,'exp2nd/oscala_%s' % typename)  #new file
    if os.path.isdir(filedir2) == True:
        shutil.rmtree(filedir2)
    os.mkdir(filedir2) 
    
    
    start=start_day
    end=end_day
        
    if start_year == end_year:
        file_dir=os.path.join(cwd+user,'experiment/%s' % str(start_year))+'/'  #old file
        print file_dir
            
        for d in range(start,end+1):
            d_str = numberToDay(d)
            goal_dir=file_dir + d_str+'/'
            goal_name = goal_dir+'oscala.'+d_str
            print 'goal_name',goal_name
            if os.path.isfile(goal_name) == True: 
                cp_cmd = "cp %soscala.%s %s/oscala.%s.%s" % (goal_dir,d_str,filedir2,str(start_year),d_str)
                print cp_cmd
                os.popen(cp_cmd)

        
    if  start_year <  end_year:
        for y in range(start_year,end_year+1):
            if(y==start_year):
                end = isLeap(y)
            elif(y==end_year):  
                start=1
            else:
                start=1
                end = isLeap(y)
            file_dir=os.path.join(cwd+user,'experiment/%s' % str(y))+'/'  #old file
            for d in range(start,end+1):
                d_str = numberToDay(d)
                goal_dir=file_dir + d_str+'/'
                goal_name = goal_dir+'oscala.'+d_str
                if os.path.isfile(goal_name) == True: 
                    print "goal_name 2"
                    os.popen("cp %s/oscala.%s %s/oscala.%s.%s" % (goal_dir,d_str,filedir2,str(y),d_str))

# type分三类： batch baseline atmosphere 
def extractFile(start_y,start_d,end_y,end_d):  

    
    filepath = os.path.join(cwd+user,'exp2nd/time_record')+'/timeRecord.txt'
    print filepath
    
    ff = open(filepath,'r')
    lastTime = ff.read()
    ff.close()
    print lastTime,
    
    strStart_d=str(start_d)
    if(len(strStart_d)==1):
        strStart_d='00'+strStart_d
    if(len(strStart_d)==2):
        strStart_d='0'+strStart_d
        
    strEnd_d=str(end_d)
    if(len(strEnd_d)==1):
        strEnd_d='00'+strEnd_d
    if(len(strEnd_d)==2):
        strEnd_d='0'+strEnd_d
        
    startTime = str(start_y)+"."+strStart_d
    print startTime
    endTime = str(end_y)+"."+strEnd_d
    print endTime
    
    if endTime > lastTime:
        if startTime > lastTime: 
           
            start_year = start_y   
            start=start_d
        else:
            tmpStartTime = lastTime.split(".")
            start_year = int(tmpStartTime[0])
            start = int(tmpStartTime[1])+1
            print tmpStartTime
        
        
        end_year = end_y
        end = end_d
        
        
        filedir1=os.path.join(cwd+user,'exp2nd')
        filedir2=os.path.join(cwd+user,'exp2nd/oscala_batch')  #new file
        print 'oscala dir', filedir2
        
        if os.path.isdir(filedir2) == False: 
            os.mkdir(filedir2)
        

        if start_year == end_year:
            file_dir=os.path.join(cwd+user,'experiment/%s' % str(start_year))+'/'  #old file
            print file_dir
            
            for d in range(start,end+1):
                d_str = numberToDay(d)
                goal_dir=file_dir + d_str+'/'
                goal_name = goal_dir+'oscala.'+d_str
                print 'goal_name',goal_name
                if os.path.isfile(goal_name) == True: 
                    cp_cmd = "cp %soscala.%s %s/oscala.%s.%s" % (goal_dir,d_str,filedir2,str(start_year),d_str)
                    print cp_cmd
                    os.popen(cp_cmd)

        
        if  start_year <  end_year:
            for y in range(start_year,end_year+1):
                if(y==start_year):
                    end = isLeap(y)
                elif(y==end_year):  
                    start=1
                else:
                    start=1
                    end = isLeap(y)
                file_dir=os.path.join(cwd+user,'experiment/%s' % str(y))+'/'  #old file
                for d in range(start,end+1):
                    d_str = numberToDay(d)
                    goal_dir=file_dir + d_str+'/'
                    goal_name = goal_dir+'oscala.'+d_str
                    if os.path.isfile(goal_name) == True: 
                        print "goal_name 2"
                        os.popen("cp %s/oscala.%s %s/oscala.%s.%s" % (goal_dir,d_str,filedir2,str(y),d_str))
                    #goal_dir=file_dir+'/'+ d_str+'/'
                    #os.popen("cp %s/oscala.* %s/oscala.%s.%s" % (goal_dir,filedir2,str(y),d_str))
        # 记录最后更新时间，这个不太准确因为万一中间断掉了，因此需要用try、expect写。交给邓家源处理！！！
        
        f = open(filepath,'w')       
        f.write(str(end_y)+"."+strEnd_d)
        f.close()
    else:
        print 'Done!'

        
       
if __name__ == '__main__':
    extractFile(2010,60,2010,64)
    #extractTempFile(2010,60,2010,63,'baseline')
    #extractTempFile(2010,60,2010,64,'atmosphere')

