#! /usr/bin/env python
#coding=utf-8
import functools,os,linecache
from subprocess import call
from django.utils.log import logging
from gps.config import CONFIG

log = logging.getLogger('utils')

unleap = [0,31,28,31,30,31,30,31,31,30,31,30,31]
leap = [0,31,29,31,30,31,30,31,31,30,31,30,31]   

def isLeap(year):
    return  ((not(year%4) and year%100) or (not(year%400))) and 366 or 365

def ymdToYd(year,month,day):
    y = int(year)
    m = int(month)
    d = int(day)

    if (isLeap(y)-366):
    	sum_day=reduce(lambda x,y:x+y,unleap[:m])
    else:
    	sum_day=reduce(lambda x,y:x+y,leap[:m])
    sum_day += d
    return {'year':year,'day':sum_day}

#显示文件
def readFile(filename):
    lines = linecache.getlines(filename)
    return lines

#修改文件
def writeFile(filename,lines):
	try:
	    f = open(filename,"w")
	    f.seek(0)
	    f.write(lines)
	    f.close()
	    return True
	except:
		log.error('An exception occured while writing into the file ')
		return False

#备份原始文件
def backupFile(filename):
    cmd = "cp -f %s %s" % (filename,filename+'.bak') 
    return call(cmd,shell=True)
     
#还原为上次备份的文件
def restoreFile(filename):
    if os.path.isfile(filename+'.bak'):
        cmd = "cp -f %s %s" % (filename+'.bak',filename)
        call(cmd,shell=True)
        return True
    else:
        log.error('Backup File not Found')
        return False

#重置为初始文件
# def reset(filename):
#     cmd = "cp -f %s %s" % (backuppath,configFilepath)
#     call(cmd,shell=True)

def getMax_MinFromFile(orgFile,counts):
    #desFile = '/home/bxy/GPS/trunk/data_results/file_tmp'
    desFile = os.path.join(CONFIG.SOFTWAREPATH,'data_results/file_tmp')
    for i in counts:
        cmd = "cat %s | awk 'BEGIN{max=-1999999;min=19999999} {if($%d>max) {max=$%d} if($%d<min) {min=$%d}} END{print max ,min}' >> %s " % (orgFile,i,i,i,i,desFile)
        os.popen(cmd)
    result=linecache.getlines(desFile)
    os.popen('rm %s' % desFile)
    return result

def mon2day(year,month):
    if (isLeap(year)-365):
        return leap[month]
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
    return doyResult

def getMbData(user,station):
    orgdir = os.path.join(SOFTWAREPATH,user,'experiment/vsoln')
    desdir = os.path.join(SOFTWAREPATH,user,'exp2nd/TimeSeries_accuracy')
    for s in station:
        s=s.upper()
        for n in range(1,4):
            desmb = 'mb_%s.dat%d' % (s,n)
            orgmb = 'mb_%s.dat%d' % (s,n)
            os.popen('cd %s ; mv %s %s ; cp -f %s %s' % (orgdir,orgmb,desmb,desmb,desdir))       
        os.popen('cd %s ; ./mbDataCollect.sh %s' % (desdir,s)) 

def changeFrame(inputFrame,outputFrame,user):
    filedir1 = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/toolkits/changeFrame/*.vel')
    filedir2 = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/toolkits/changeFrame/result')
    os.popen("rm %s/*.vel" % filedir2)
    files = glob.glob(filedir1)
    for f in files:
        (filepath,filename) = os.path.split(f)
        cmd = 'cvframe %s %s/%s %s %s' %(f,filedir2,filename,inframe,outframe)
        os.system(cmd)
    
    zippath = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/toolkits/changeFrame')
    zip_cmd = "cd %s ; zip -r data.zip result" % (zippath)
    os.popen(zip_cmd)

def numToDay(d):
    return "%03d"%d

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
    return d

class teqc(object):
    """just for teqc"""
    def readfile(rfile):
        tmp = os.path.join(CONFIG.SOFTWAREPATH,'data_results/data_tmp')
        os.popen(" awk '{if($1~/^SUM/) print $0}' %s > %s " % (rfile,tmp)) 
        context=open(tmp,'r').read()    
        li=context.split()
        context= [li[12], li[14], li[15]]
        return context

from __future__ import division        
class GetBaselineData(object):
    """docstring for GetBaselineData"""
    def getData(typename):
        baseline_path = ''
        if typename == 'baseline':
            baseline_path=os.path.join(cwd,'exp2nd/baseline')
            filepath = os.path.join(baseline_path,'baseline.dat')
            if os.path.isfile(filepath):
                os.remove(filepath)      
        elif typename == 'batch':
            baseline_path=os.path.join(cwd,'exp2nd/baseline_batch')  
            
        oscala_path=os.path.join(cwd,'exp2nd/oscala_%s/oscala.*' % typename)
            
        list_files = os.popen("dir %s" % oscala_path).read().split() 
        list_files.sort()  #按时间顺序排列文件
        
        for l in list_files:
            cmd = "awk '{if($2~/[0-9]X$/ && $3~/N/) print $0}' %s >> %s/baseline.dat" %(l,baseline_path)
            os.popen(cmd)
       
def checktime(p):
    pathlist = os.listdir(p)
    extlist = ['csv','sum','out','LC','status','fatal','warning']
    
    for i in range(len(pathlist)):
    
        source=p+'/'+pathlist[i]
        if os.path.isfile(source):
            m=time.localtime(os.stat(source).st_ctime) #文件创建时间
            
            starttime = datetime.datetime.now() #当前时间
            endtime = datetime.datetime(m.tm_year,m.tm_mon,m.tm_mday,m.tm_hour,m.tm_min,m.tm_sec)
            
            mydays=(starttime-endtime).days  #计算时间间隔
            #print mydays
            ext=source.split('.')[-1]  #文件后缀名
            
            if mydays>=1 and ext in extlist:
                #一天清空一次
                os.remove(source)
