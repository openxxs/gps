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
	if os.path.isfile(filename+'.bak')
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
    print doyResult
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

def extractFile(start_y,start_d,end_y,end_d):
    pass 
