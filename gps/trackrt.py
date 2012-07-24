#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os,glob
import commands
import shutil
import time
from gps.config import CONFIG
#前台输入项
ref_site=''    #参考站
pro_site=''    #目标站
csv_time=''    #csv生成时间段包括  00:00 , 06:00 , 12:00 , 18:00

flag=True      #判断今天sp3文件是否更新过的标志

#cwd=os.path.dirname(__file__) 
cwd=CONFIG.SOFTWAREPATH
#print cwd

#1.关于trackRT命令若表明-d xxx xxx xxx 则处理这几个站，若不标明则不处理 用循环做？？
#cmd = "trackRT -p 1100 -r %s -d %s -f trackRT_pbo.cmd -n %s" % (refstate, statelist, refstate)
#2.把refestate去修改.cmd中的参考站名
#3.执行trackRT前检查.sp3文件是否更新，（用test.sh）因为不更新就会出错！！！
#4.使用由trackRT生成的.csv文件
 
def command(): 
    global ref_site, pro_site
    #修改配置文件模板
    #sampledir = "/home/bxy/GPS/trunk/trackRT_sample"
    sampledir = os.path.join(cwd,'trackRT_sample')
    #cmddir = os.path.join(cwd,'trackRT_cmd')
    #cmddir = "/home/bxy/GPS/trunk/templates/amstock"
    cmddir = os.path.join(cwd,'templates/amstock')
    
    ref_in_file = '"     %s"' % ref_site
    print ref_in_file
    modify = "awk '$1~/^@/{$1=%s};{print $0}' %s/trackRT_pbo.cmd.sample > %s/trackRT_pbo.cmd" % (str(ref_in_file), sampledir, cmddir)
    print modify
    os.popen(modify)
    
    #判断当天的sp3文件是否更新了 01 5-24/6 * * * csh /home/bxy/trunk/cron.sp3u > /dev/null 2>&1 (已经在系统中设置) ？？？？？？？？？？
    
    #生成.LC文件
    #设置trackRT命令
    
    port = '1100'
    
    cmd = "cd %s ; trackRT -p %s -r %s -d %s %s -f trackRT_pbo.cmd -n %s " % (cmddir,port, ref_site, ref_site,pro_site,ref_site) #配置文件地址有问题2.不知道为什么-d后面必须添上参考站名 该命令用于后台执行
    os.popen(cmd)
    
    
#用于将生成的csv文件名写入amstock_settings.xml中

def trackrt(dst,ext):
    #getInput(dst,ext)
    global ref_site, pro_site
    ref_site = dst
    pro_site = ext
    command()   
    
if __name__ == '__main__':
    trackrt('CHZZ','CABL')
    #getPic()
