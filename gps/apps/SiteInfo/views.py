#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
#from trunk.fileshandle import fileshandle
#from trunk.data_process import readDst
import commands
import os,sys,re,shutil,linecache,glob,logging
import time
from gps.config import CONFIG
from models import Site,Img
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#import getMax_Min

from django.utils.log import logging
#cwd=os.path.dirname(__file__)
cwd=CONFIG.SOFTWAREPATH

png1=''
png2=''
png3=''
png4=''

def initlog(): 
    logger = logging.getLogger()
    hdlr = logging.FileHandler('SiteInfo.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

log = initlog


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
    sitelist=Site.objects.all()
    sitenameList = [site.Code for site in sitelist]
    siteList,page_range=my_pagination(request,sitelist)
    return render_to_response("SiteInfo/siteList.html",{'siteList':siteList,'sitenameList':sitenameList,'page_range':page_range},context_instance=RequestContext(request))
    
def dataManaging(request):  #台站质量
    sitelist=Site.objects.all()
    sitenameList = [site.Code for site in sitelist]
    siteList,page_range=my_pagination(request,sitelist)
    return render_to_response("SiteInfo/dataManage.html",{'siteList':siteList,'sitenameList':sitenameList,'page_range':page_range},context_instance=RequestContext(request))

def Map(request):           #台站分布
    return render_to_response("SiteInfo/map.html",{},context_instance=RequestContext(request))

def sitebase(request,sitecode=None):     #台站列表中的某个台站
    if not sitecode:
        try:
            sitecode=request.POST.get('sitecode')
        except:
            raise Http404
    siteList = Site.objects.filter(Code=sitecode)
    site = siteList.count() and siteList[0] or False
    return render_to_response("SiteInfo/siteBase.html",{'site':site},context_instance=RequestContext(request))
    
        
def update(request,sitecode):
    is_success=False
    _request=request
    is_success=fileshandle(_request,sitecode)
    time.sleep(2)    
    if is_success:
        update_singal(sitecode)
        return render_to_response('data_update.html',{'png1':png1,'png2':png2,
                                  'png3':png3,'png4':png4,'error':False},context_instance=RequestContext(request))
    else:
        update_singal(sitecode)
        return render_to_response('data_update.html',{'png1':png1,'png2':png2,
                                  'png3':png3,'png4':png4,'error':True},context_instance=RequestContext(request))

def update_All(request):
    sitelist=Site.objects.all()
    _request=request
    for sitecode in sitelist :
        if len(sitecode.Code)==4 :
            is_success = fileshandle(_request,sitecode.Code)
            if is_success:
                time.sleep(2)
                update_singal(sitecode.Code)
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
    return render_to_response('update.html',{'info':info},context_instance=RequestContext(request)) 
    
      
def data(request,sitecode=None):
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
    return render_to_response("data.html",{'png1':png1,'png2':png2,
                                    'png3':png3,'png4':png4,'site':site},context_instance=RequestContext(request))

def updatephoto(png,sitecode,fileName):
    obfile = os.path.join(cwd,'data_results/%s/%s' % (sitecode,fileName))
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
    cmd = 'psxy %s  -JX6.5/2.0 -R%s/%s/%s/%s -Ba0.5f0.1:"":/a%0.2ff5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i >%s' % (obfile,minTime,maxTime,minValue,maxValue,dis,os.path.join(cwd,'temp.pdf'))
    outinfo=commands.getstatusoutput(cmd) 
                                          
    if outinfo[0]!=0 or outinfo[1]:
        log.error('errors pdf \n')
    outinfo=commands.getstatusoutput('convert -trim %s %s' % (os.path.join(cwd,'temp.pdf'),os.path.join(cwd,png[1:])))
    if outinfo[0]!=0 or outinfo[1]:
        log.error('errors png \n')
    else:    
        commands.getoutput('rm %s' % os.path.join(cwd,'temp.pdf'))
# Create your views here.
def my_pagination(request, queryset):
    display_amount=15     
    after_range_num = 5
    bevor_range_num = 4 
    paginator = Paginator(queryset, display_amount)
    try:         
        page =int(request.GET.get('page'))
    except:
        page = 1
    try:                                         
        objects = paginator.page(page)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)
    #except PageNotAnInteger: 
    # If page is not an integer, deliver first page.
    #    objects = paginator.page(1)
    except:
        objects = paginator.page(1)
    # 显示范围                           
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:page+bevor_range_num]
    return objects,page_range
