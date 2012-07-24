#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response
import commands
import os,sys,re,shutil,linecache
import datetime
from django.template import RequestContext
from gps.apps.DataProc.views import readDst
#from trunk.data_process import readDst
#import atmosphereAccuracy
#import atmosphereView
#import baselineAccuracy
#import baselineView
#import timeSeriesAccuracy

#cwd=os.path.dirname(__file__)
cwd=os.getcwd()

username=''
error=''

linkPath='exp3nd/linkTS_Example/'
yr1=''
mon1=''
day1=''
yr2=''
mon2=''
day2=''
stn=''
trend=''
source=''

        
def initParameter(request):
    global yr1,mon1,day1,yr2,mon2,day2,trend,stn
    yr1      =   (request.GET['startYear'])
    mon1     =   (request.GET['startMonth'])
    day1     =   (request.GET['startDay'])
    yr2      =   (request.GET['endYear'])
    mon2     =   (request.GET['endMonth'])
    day2     =   (request.GET['endDay'])
    trend    =   (request.GET['trend'])
    stn      =   request.GET['dst_station']
    if(len(mon1)==1):
        mon1='0'+mon1
    if(len(mon2)==1):
        mon2='0'+mon2
    if(len(day1)==1):
        day1='0'+day1
    if(len(day2)==1):
        day2='0'+day2

def showParameter():
    print yr1,mon1,day1
    print yr2,mon2,day2
    print stn

    
def timeSeries(request):
    dstList=readDst(request.user.username)
    return render_to_response("ResultView/timeSeries.html",{'dstList':dstList},context_instance=RequestContext(request))

def velocities(request):
    dstList=readDst(request.user.username)
    print 'cd %s ; cp -f ../result.vel . ; ./draw.sh ;  cp -f  vel.png ../vel.png ; rm vel.png result.vel ; ' % os.path.join(cwd,'exp2nd/vel_result/draw')
    os.popen('cd %s ; cp -f ../result.vel . ; ./draw.sh ;  cp -f  vel.png ../vel.png ; ' % os.path.join(cwd,'exp2nd/vel_result/draw'))      #bxy 2012 1 2 11:08   bxy 2012 1 6 12:41 添加两个 rm
    #os.popen('cd %s ; cp -f ../result.vel . ; ./draw.sh ; rm vel.ps ;  cp -f ./vel.ps* ../vel.ps ;rm ./vel.ps*' % os.path.join(cwd,'exp2nd/vel_result/draw'))
    #os.popen('cd %s ; convert -trim vel.ps vel.png ; rm vel.ps' % os.path.join(cwd,'exp2nd/vel_result'))
    return render_to_response("ResultView/velocities.html",{'file':'/exp2nd/vel_result/result.vel',
                               'png':'/exp2nd/vel_result/vel.png','username':username,'error':error},context_instance=RequestContext(request))
                               
def baselineCheck(request):
    dstList=readDst(request.user.username)
    return render_to_response("ResultView/baselineCheck.html",{'dstList':dstList,'username':username,'error':error},context_instance=RequestContext(request))
def atmosphereZenithDelay(request):
    dstList=readDst(request.user.username)
    return render_to_response("ResultView/atmosphereZenithDelay.html",{'dstList':dstList,'username':username,'error':error},context_instance=RequestContext(request))
    
def resultApx(request):
    return render_to_response("ResultView/resultApx.html",{},context_instance=RequestContext(request))
    
def Draw_rApx_pictures(request):
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    selectType = request.GET['selectType']
    if(selectType=='0'):
        print '时间序列'
        initParameter(request)
        showParameter()
        timeSeriesAccuracy.timeSeriesAccuracy(stn,yr1,mon1,day1,yr2,mon2,day2,now,username)
        filepath=CONFIG.SOFTWAREPATH+username+'/exp2nd/TimeSeries_accuracy/temp/'
        filename='timeSeriesAccuracy'+now
        tsfiles=[filepath+filename+'.E',filepath+filename+'.N',filepath+filename+'.U']
        pngs=[filepath+filename+'.E.png',filepath+filename+'.N.png',filepath+filename+'.U.png']
        return render_to_response("png_tsAccuracy.html",{'files':tsfiles,'pngs':pngs},context_instance=RequestContext(request))
    if(selectType=='1'):
        print '基线精度'
        initParameter(request)
        showParameter()
        #stns=stn.split("_")
        stns=stn.split()
        print stns
        baselineAccuracy.baselineAccuracy(stns[0],stns[1],yr1,mon1,day1,yr2,mon2,day2,now)
        filepath='/exp2nd/baseline_accuracy/temp/'
        filename = 'baselineAccuracy'+now
        bsfiles=[filepath+filename+'.E',filepath+filename+'.N',filepath+filename+'.U',filepath+filename+'.L']
        pngs=[filepath+filename+'.E.png',filepath+filename+'.N.png',filepath+filename+'.U.png',filepath+filename+'.L.png']
        return render_to_response("png_bsAccuracy.html",{'files':bsfiles,'pngs':pngs},context_instance=RequestContext(request))
    if(selectType=='2'):
        print '大气延迟'
        initParameter(request)
        showParameter()
        
        print stn,yr1,mon1,day1,yr2,mon2,day2,now
        atmosphereAccuracy.atmosphereAccuracy(stn,yr1,mon1,day1,yr2,mon2,day2,now)
        filepath='/exp2nd/atmosphere_accuracy/temp/'
        atmfile = filepath+now+'atmosphereAccuracy.dat'
        pngpath = filepath+now+'image.png'
        return render_to_response("ResultView/png_atmosphereZenithDelay.html",{'file':atmfile,'png':pngpath},context_instance=RequestContext(request))
                               
def Draw_azDelay_pictures(request):
    
    initParameter(request)
    showParameter()
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    atmosphereView.atmosphereView(stn,yr1,mon1,day1,yr2,mon2,day2,now)
    return render_to_response("ResultView/png_atmosphereZenithDelay.html",{'file':'/exp2nd/atmosphere_view/temp/'+now+'atmosphere.dat','png':'/exp2nd/atmosphere_view/temp/image'+now+'.png'},context_instance=RequestContext(request))

def Draw_bs_pictures(request):
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    initParameter(request)
    showParameter()
    stns=stn.split("_")
    print stns
    baselineView.baselineView(stns[0],stns[1],yr1,mon1,day1,yr2,mon2,day2,request.GET['source'],now)
    filepath='/exp2nd/baseline_view/temp/'
    filename = 'baseline'+now
    bsfiles=[filepath+filename+'.E',filepath+filename+'.N',filepath+filename+'.U',filepath+filename+'.L']
    pngs=[filepath+filename+'.E.png',filepath+filename+'.N.png',filepath+filename+'.U.png',filepath+filename+'.L.png']
    return render_to_response("ResultView/png_baselineCheck.html",{'files':bsfiles,'pngs':pngs},context_instance=RequestContext(request))

def Draw_ts_pictures(request):
#   用Gamitdata_analysing()里处理出的数据画时间序列和速度场
#   vsoln文件夹里存放结果文件和生成的图片
    global yr1,mon1,day1,yr2,mon2,day2,trend,stn
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    initParameter(request)
            
#   目标文件初始化以及链入配置文件
    os.popen("cd %s ; mkdir vsoln " % os.path.join(cwd,'exp2nd'))
    vsoln_path=os.path.join(cwd,'vslon')
    try:     
        os.popen(' ln -s '+os.path.join(cwd,(linkPath+'globk_comb.cmd'))+' '+ os.path.join(cwd,'exp2nd/vsoln/globk_comb.cmd')+
              ' ; ln -s '+os.path.join(cwd,(linkPath+'globk_vel.cmd'))+' ' + os.path.join(cwd,'exp2nd/vsoln/globk_vel.cmd') +
              ' ; ln -s '+os.path.join(cwd,(linkPath+'glorg_comb.cmd'))+' '+ os.path.join(cwd,'exp2nd/vsoln/glorg_comb.cmd')+
              ' ; ln -s '+os.path.join(cwd,(linkPath+'glorg_vel.cmd'))+' ' + os.path.join(cwd,'exp2nd/vsoln/glorg_vel.cmd'))
    except Exception:
        ei  = open(os.path.join(cwd,'info/!exp_errorInfo'),'a')
        ei.write("%s: After processing by command sh_gamit,linking file error!\n" %  datetime.datetime.now())   
        ei.close()      
                
#   结果处理，由sh_plotcrd得到时间序列结果
#   sh_plotcrd 参数中-s long控制横坐标的跨度大，默认default为short，跨度小，-mb生成mb文件，从中提取结果
    os.popen("cd %s ; mkdir hfile_in_proc ; " % os.path.join(cwd,'exp2nd'))
    fins = open(os.path.join(cwd,'exp2nd/ins'), 'w+')
    fins.write(' '+stn)
    fins.close()
    
    hfilelist = os.listdir(os.path.join(cwd,'exp2nd/h_results'))
    Time_min = yr1+mon1+day1
    Time_max = yr2+mon2+day2
    stn=stn.upper()
    print yr1
    print day1
    print mon1

#   提取指定时间段的h文件                                                          \
    for hfname in hfilelist:
        if len(hfname)  >= 7:
            if (int)(hfname[1:7]) >= (int)(Time_min) and (int)(hfname[1:7]) <= (int)(Time_max):
                os.popen('cp '+os.path.join(cwd,'exp2nd/h_results/%s ' % hfname)+os.path.join(cwd,'exp2nd/hfile_in_proc'))   
    try:
        os.popen('cd %s ; ls ../hfile_in_proc/h*glx > scal.gdl ; glred 6 globk_comb.prt globk_comb.log scal.gdl globk_comb.cmd ;  sh_plotcrd -f globk_comb.org -res -o %s -vert -col 1 -mb -b ../ins ;' % (os.path.join(cwd,'exp2nd/vsoln'),trend)) 
    except Exception:
        ei  = open(os.path.join(cwd,'info/!exp_errorInfo'),'a')
        ei.write("%s: Processing by command sh_plotcrd or sh_plotvel wrong!\n" % datetime.datetime.now())   
        ei.close()
        
    for n in range(1,4):
        os.popen('cd %s ; mv mb_%s_???.dat%d mb_%s.dat%d' % (os.path.join(cwd,'exp2nd/vsoln'),stn,n,stn+now,n))        
    os.popen('cd %s ; cp -f ./mb_%s.dat* %s' % (os.path.join(cwd,'exp2nd/vsoln'),stn+now,os.path.join(cwd,'exp2nd/TimeSeries_result')))
    os.popen('cd %s ; ./mbDataCollect.sh mb_%s.dat' % (os.path.join(cwd,'exp2nd/TimeSeries_result'),stn+now))
    os.popen("cd %s ; convert -trim -crop 595x842+0+50 psbase_ensum.%s* ../../exp2nd/TimeSeries_result/%s.png" % (os.path.join(cwd,'exp2nd/vsoln'),stn,stn+now))
    os.popen('cd %s ; rm -r hfile_in_proc ; rm -r vsoln;' % os.path.join(cwd,'exp2nd'))
    return render_to_response("ResultView/png_timeSeries.html",{'png':('/exp2nd/TimeSeries_result/%s.png' % stn+now),'file':('/exp2nd/TimeSeries_result/mb_%s.dat' % (stn+now))},context_instance=RequestContext(request))
 
       

# Create your views here.
