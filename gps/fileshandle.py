#! /usr/bin/env python
#coding=utf-8
import commands,os,glob
from teqc import readfile
#from django.http import HttpResponse,HttpRequest
import datetime
import time
from gps.config import CONFIG
#cwd=os.path.dirname(__file__)        #获取当前路径，也就是站点的根目录 
cwd=CONFIG.SOFTWAREPATH

def judge_mkdir(dirpath):
    if os.path.isdir(dirpath)==False:
        os.mkdir(dirpath)
        
def fileshandle(request,sitecode):        
    op_result=True         #操作更新的结果，初始化为True
    firstpath=os.path.join(cwd,'data/%s/*.Z' % sitecode)        #用正则表达式，获取data文件夹下的所有.Z原始数据
    firstfiles=glob.glob(firstpath)
    if len(firstfiles)==0:
        return False
    try:
        userInfo_file=open(os.path.join(cwd,'info/userInfo.txt'),'a')     #存储用户信息的文件
        errorInfo_file=open(os.path.join(cwd,'info/errorInfo.txt'),'a')   #存储错误信息的文件
        return_file=open(os.path.join(cwd,'info/returnsInfo.txt'),'w')    #存储用户操作状态的返回信息
        #logRecord_file = open(os.path.join(cwd,'log/date.txt'),'a')
        localtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        log_file = open(os.path.join(cwd,'log/%s.log' % localtime),'a')
        
        judge_mkdir(os.path.join(cwd,'data_results/%s' % sitecode))
        
        mp1_file=open(os.path.join(cwd,'data_results/%s/mp1.txt' % sitecode ),'a')
        mp2_file=open(os.path.join(cwd,'data_results/%s/mp2.txt' % sitecode ),'a')
        have_file=open(os.path.join(cwd,'data_results/%s/#have.txt' % sitecode ),'a')
        time_file=open(os.path.join(cwd,'data_results/%s/time.txt' % sitecode ),'a')
    except IOError,Exception:
        errorInfo_file.write("%s: 某个关键文件不存在或发送错误，更新无法进行！" % datetime.datetime.now())
        userInfo_file.close() 
        errorInfo_file.close()            
        return_file.close()
        mp1_file.close()
        mp2_file.close()
        time_file.close()
        have_file.close()
        return False
    max_day=0
        

    #遍历原始数据，逐一进行处理
    for t in range(0,len(firstfiles)):
        data_path=os.path.join(cwd,'data/%s/*' % sitecode)
        backup_path=os.path.join(cwd,'backup_data/%s/' % sitecode)
        if (os.path.isdir(backup_path))==False:
            os.mkdir(backup_path)
        outinfo=commands.getstatusoutput('cp -r -b -f %s %s' % (data_path,backup_path))  #处理前，先将原始数据备份，以便后面的数据重新处理和异常处理
        
        if outinfo[0]!=0 or outinfo[1]:                                         #对这条命令的异常进行分析、记录处理
            errorInfo_file.write('%s: there are some errors when file backup.It may be some unusual operation so that there is not a folder named data or backup_data! \n' % datetime.datetime.now())
            return_file.write('The server has important concerns, please promptly Contact administrator! \n')
            userInfo_file.close() 
            errorInfo_file.close()            
            return_file.close()
            mp1_file.close()
            mp2_file.close()
            time_file.close()
            have_file.close()
            return False
        
        #commands.getoutput("cd %s" % cwd);
        outinfo=commands.getstatusoutput('cd %s ; sh_crx2rnx -f %s' % (cwd,firstfiles[t]))   #用sh_crx2rnx对原始数据.05d.Z文件进行第一步处理，得到同名的.05o文件
        
        '''  经过一次路径分割，两次分割拓展名分割，得到文件名filename '''
        (filepath,_file)=os.path.split(firstfiles[t])
        (_file,ext)=os.path.splitext(_file)
        (filename,ext)=os.path.splitext(_file)
        
        if outinfo[0]!=0 or outinfo[1]:
            if outinfo[0]==0:
                errorInfo_file.write('%s: （sh_crx2rnx命令）结果 %d:   \n %s \n' % (datetime.datetime.now(),outinfo[0],outinfo[1]))
            else:
                errorInfo_file.write('%s: （sh_crx2rnx命令）错误类型  %d:   \n %s \n' % (datetime.datetime.now(),outinfo[0],outinfo[1]))           
            print _file
            return_file.write(_file)
            return_file.write(':fail to update，please promptly Contact administrator!\n')
            op_result=False

        else:
            secondfile=os.path.join(cwd,('%s.%so' % (filename,ext[1:3])))    #在当前目录下，找到第一步处理后生成的文件名
            #commands.getoutput("cd %s" % cwd);
            outinfo=commands.getstatusoutput('teqc +qc -O.int 30.0 -plot %s' % secondfile)   #对生成的文件，用teqc命令进行第二步处理
            
            if outinfo[0]!=0 :               
                errorInfo_file.write('%s: （teqc命令）错误类型  %d:   \n %s \n' % (datetime.datetime.now(),outinfo[0],outinfo[1]))  
                return_file.write(_file)
                return_file.write(' fail to update,please promptly Contact administrator!\n')
                
                op_result=False
                
            else:
                rinexpath = os.path.join(cwd,'rinex/%s' % sitecode)
                if (os.path.isdir(rinexpath))==False:
                    os.mkdir(rinexpath)
                commands.getoutput('mv %s %s' % (secondfile,rinexpath))
                thirdfile=os.path.join(cwd,('%s.%sS' % (filename,ext[1:3])))    #在当前目录下，找到第二步处理后的文件名
                num1=(int)(ext[1:3])
                num2=((int)(filename[4:7]))/360.0
                num=num1+num2     
                if num > max_day:
                    max_day=num           
                context=readfile(thirdfile)  
                have_file.write('20%.4f %s 0\n' % (num,context[0]))
                mp1_file.write('20%.4f  %s 0\n' % (num,context[1]))
                mp2_file.write('20%.4f  %s 0\n' % (num,context[2]))
                time_file.write('20%.4f %d 0\n' % (num,1))
                return_file.write(_file)
                return_file.write(' update succeed！\n')
                commands.getoutput('rm %s' % thirdfile)
                
    if op_result:
        userInfo_file.write('%s: %s has updated the data successfully,you can reference to returns_Info.txt\n' % (datetime.datetime.now(),request.META['REMOTE_ADDR']))
        log_file.write('%s: %s has updated the data successfully,you can reference to returns_Info.txt\n' % (datetime.datetime.now(),request.META['REMOTE_ADDR']))
        return_file.close()
        return_file=open(os.path.join(cwd,'info/returnsInfo.txt'),'r')
        log_file.write(return_file.read())
        '''logfiles = os.listdir(cwd,'log')
        for log in logfiles:
            
        #logRecord_file.write("%s.log \n" % localtime)
        logRecord_file.writelines(logfiles)'''
    else:
        userInfo_file.write('%s: %s failed to update,you can reference to returns_Info.txt and errorInfo.txt\n' % (datetime.datetime.now(),request.META['REMOTE_ADDR']))
    commands.getoutput('rm %s' % os.path.join(cwd,'data/%s/*' % sitecode))       
    userInfo_file.close() 
    errorInfo_file.close()            
    return_file.close()
    mp1_file.close()
    mp2_file.close()
    time_file.close()
    have_file.close()
    return True
if __name__=='__main__':
    fileshandle('','brdc')

