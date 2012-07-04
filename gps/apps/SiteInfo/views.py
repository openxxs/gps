#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from trunk.fileshandle import fileshandle
from trunk.data_process import readDst
import commands
import os,sys,re,shutil,linecache,glob
import time
import getMax_Min

#cwd=os.path.dirname(__file__)
cwd=os.getcwd()

png1=''
png2=''
png3=''
png4=''

username=''
error=''

def checkUser(request):
    global username,error
    if 'error' in request.GET:
        error=request.GET['error']
    else:
        error=''
    if request.user.is_authenticated():
        username=request.user
    else:
        username=''
    print username,error

class Site:                #站点信息类
    def __init__(self,_code,_name,_longitude,_latitude,_intro="",_imgList=[]):
        self.code=_code
        self.name=_name
        self.longitude=_longitude
        self.latitude=_latitude
        self.intro=_intro
        self.imgList=_imgList
                
def siteSearch(request):
    #sitelist=readDst()
    Dst=request.GET['siteCode']
    return HttpResponseRedirect('/siteInfo/data/%s' % Dst)  
    
def readInfo(type):         #type==0,读取站点全部信息;#type==1,只读取站点代号code

    sitelist=[]
    p_sitesInfo=open(os.path.join(cwd,'site_list/sitesinformation'),'r')
    sitesInfo=p_sitesInfo.readlines()
    p_sitesInfo.close()
    for line in sitesInfo:
        info=line.split()
        if len(info)>0:
            if(type==0):    
                site=Site(info[0],info[1],info[2],info[3])
            elif(type==1):    
                site=info[0]
            sitelist.append(site)
    return sitelist

def rw_count(sitecode):     #更新和读取站点对应的count值    
    countFile = os.path.join(cwd,'site_list/%s/png/count.txt' % sitecode)
    count=0
    if os.path.isfile(countFile)==False:
        count=0
    else:
        count_file=open(countFile,'r')
        count=(int)(count_file.read())
        count_file.close()        
        pngPath = os.path.join(cwd,'site_list/%s/png' % sitecode)
        os.popen(' cd %s ; rm *.png ' % pngPath)
    count=count+1
    count_file=open(countFile,'w')
    count_file.write('%d' % count)
    count_file.flush()
    count_file.close()
    return count

def sitesList(request):      #台站列表
    sitelist=readInfo(0)
    checkUser(request)
    
    p=open(cwd+"/t","w+")
    p.write(cwd)
    p.close()
    return render_to_response("siteList.html",{'siteList':sitelist,'username':username,'error':error})
    
def dataManaging(request):  #台站质量
    sitelist=readInfo(0)
    checkUser(request)
    return render_to_response("dataManaging.html",{'siteList':sitelist,'username':username,'error':error})

def log(request):           #台站信息更新及log
    logList=[]
    logfilepath = os.path.join(cwd,'log/*.log')
    logfiles = glob.glob(logfilepath)
    '''p_logInfo=open(os.path.join(cwd,'log/date.txt'),'r');
    for log in p_logInfo:
        logList.append(log[0:-1])
    p_logInfo.close()'''
    for logfile in logfiles:
        (filepath,filename)=os.path.split(logfile)
        logList.append(filename)
    checkUser(request)
    return render_to_response("log.html",{'logList':logList,'username':username,'error':error})

def Map(request):           #台站分布
    checkUser(request)
    return render_to_response("map.html",{'username':username,'error':error})

def sitebase(request,sitecode):     #台站列表中的某个台站
    p_siteInfo=open(os.path.join(cwd,'site_list/%s/information' % sitecode),'r')
    siteInfo=p_siteInfo.read().split()
    p_siteInfo.close()

    p_siteIntro=open(os.path.join(cwd,'site_list/%s/introduction' % sitecode),'r')
    siteIntro=p_siteIntro.read()
    site_pc=os.listdir(os.path.join(cwd,'site_list/%s/pictures' % sitecode))

    #site=Site(temp['code'],temp['name'],temp['longitude'],temp['latitude'],siteIntro,site_pc)
    site=Site(siteInfo[0],siteInfo[1],siteInfo[2],siteInfo[3],siteIntro,site_pc)
    checkUser(request)
    return render_to_response("siteBase.html",{'site':site,'username':username,'error':error})
    
        
def update(request,sitecode):
    is_success=False
    _request=request
    is_success=fileshandle(_request,sitecode)
    time.sleep(2)    
    if is_success:
        update_singal(sitecode)
        return render_to_response('data_update.html',{'png1':png1,'png2':png2,
                                  'png3':png3,'png4':png4,'error':False})
    else:
        update_singal(sitecode)
        return render_to_response('data_update.html',{'png1':png1,'png2':png2,
                                  'png3':png3,'png4':png4,'error':True})

def update_All(request):
    sitelist=readInfo(1)
    print sitelist
    _request=request
    for sitecode in sitelist :
        if len(sitecode)==4 :
            is_success = fileshandle(_request,sitecode)
            if is_success:
                time.sleep(2)
                update_singal(sitecode)
    '''  台站信息更新日志  '''
    return HttpResponse("successful")
def update_singal(sitecode):
    global png1,png2,png3,png4
    count=rw_count(sitecode)
    png1='/site_list/%s/png/1%d.png' % (sitecode,count)
    updatephoto(png1,sitecode,'time.txt')
    png2='/site_list/%s/png/2%d.png' % (sitecode,count)
    updatephoto(png2,sitecode,'#have.txt')
    png3='/site_list/%s/png/3%d.png' % (sitecode,count)
    updatephoto(png3,sitecode,'mp1.txt')
    png4='/site_list/%s/png/4%d.png' % (sitecode,count)
    updatephoto(png4,sitecode,'mp2.txt')
    
def updateInfo(request):
    info=[]
    try:
        errorInfo_file=open(os.path.join(cwd,'info/errorInfo.txt'),'a') 
        return_file=open(os.path.join(cwd,'info/returnsInfo.txt'),'r')    
        for line in return_file:
            info.append(line[0:-1])  #去掉\n，在html里面\n无法识别，会出异常
        return_file.close()
        if len(info)>10:
            info = info[0:9]
            info.append('.')
            info.append('.')
            info.append('.')
    except IOError:
        errorInfo_file.write("访问returnsInfo.txt时候错误\n")
        info.append("读取更新信息失败，访问信息文件是错误，请联系管理员")
    return render_to_response('update.html',{'info':info}) 
    
      
def data(request,sitecode):
    global png1,png2,png3,png4
    count_file=open(os.path.join(cwd,'site_list/%s/png/count.txt' % sitecode),'r')
    count=(int)(count_file.read())
    print ('%d' % count)
    count_file.close()
    png1='/site_list/%s/png/1%d.png' % (sitecode,count)
    png2='/site_list/%s/png/2%d.png' % (sitecode,count)
    png3='/site_list/%s/png/3%d.png' % (sitecode,count)
    png4='/site_list/%s/png/4%d.png' % (sitecode,count)
    p_siteInfo=open(os.path.join(cwd,'site_list/%s/information' % sitecode),'r')
    siteInfo=p_siteInfo.read().split()
    p_siteInfo.close()
    site=Site(siteInfo[0],siteInfo[1],siteInfo[2],siteInfo[3])
    print site
    checkUser(request)
    return render_to_response("data.html",{'png1':png1,'png2':png2,
                                    'png3':png3,'png4':png4,'site':site,'username':username,'error':error})

def updatephoto(png,sitecode,fileName):

    errorInfo_file=open(os.path.join(cwd,'info/errorInfo.txt'),'a') 
    obfile = os.path.join(cwd,'data_results/%s/%s' % (sitecode,fileName))
    print obfile
    scope = getMax_Min.getMax_MinFromFile(obfile,[1,2])
    times_scope = scope[0].split()
    value_scope = scope[1].split()
    maxTime = "%d" % (float(times_scope[0])+1)
    minTime = "%d" % float(times_scope[1])
    maxValue = "%d" % (float(value_scope[0]))
    maxValue = "%d" % ( float(value_scope[0]) + 10**(len(maxValue)-1))
    minv = float(value_scope[1])
    minValue=''
    if minv>0 :       
        minValue = "-%d" % minv
    else:
        minValue = "%d" % minv
    dis = float(maxValue)/5.0
    print dis
    cmd = 'psxy %s  -JX6.5/2.0 -R%s/%s/%s/%s -Ba0.5f0.1:"":/a%0.2ff5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i >%s' % (obfile,minTime,maxTime,minValue,maxValue,dis,os.path.join(cwd,'temp.pdf'))
    print cmd
    outinfo=commands.getstatusoutput(cmd) 
                                          
    if outinfo[0]!=0 or outinfo[1]:
        errorInfo_file.write('errors pdf \n')
    outinfo=commands.getstatusoutput('convert -trim %s %s' % (os.path.join(cwd,'temp.pdf'),os.path.join(cwd,png[1:])))
    if outinfo[0]!=0 or outinfo[1]:
        errorInfo_file.write('errors png \n')
    else:    
        commands.getoutput('rm %s' % os.path.join(cwd,'temp.pdf'))
# Create your views here.
