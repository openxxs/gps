#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.models import User
from django.utils.log import logging
from django.template import RequestContext

import sys, datetime, json, commands, os, re, shutil, linecache, glob, copy, threading, time,logging
from subprocess import *

#import extractOscalaFile
#import getBaselineData
#import getAtmosphereData
#import getMbData
#
import gps.track
import gps.trackrt

from gps.config import CONFIG
from gps.utils import isLeap,readFile,writeFile,ymdToYd

from forms import *

from gps import kmp

#import ion
#import modifyText
#import monthToDay

#from dataDownload import intervel

def initlog(): 
    logger = logging.getLogger()
    hdlr = logging.FileHandler('DataProc.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

log = initlog()

GAMITTABLE = CONFIG.GAMITTABLEPATH
SOFTWAREPATH = CONFIG.SOFTWAREPATH
RINEXPATH = CONFIG.RINEXPATH
fileList = CONFIG.fileList.split('%%')
downloadList = CONFIG.downloadList.split('%%')
refStation = CONFIG.refStation

cwd = SOFTWAREPATH

#trackRT部分

tasksNum = 0
tasks    = []

@login_required()
def datatrack(request):
    form = TrackForm()
    user = request.user.username
    if request.method=="POST":
        form = TrackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            sYear = data['sYear']
            sMonth = data['sMonth']
            sDay = data['sDay']
            sHour = data['sHour']
            eHour = data['eHour']
            sites = data['sites'].split()
            days = ymdToYd(sYear, sMonth, sDay)
            filedir = os.path.join(CONFIG.SOFTWAREPATH+user, 'track/track_data')
            cmd = "cd %s;csh %s/get_orbits -archive sopac -yr %s -doy %s -ndays 1" % (filedir, cwd, sYear, days)
            call(cmd, shell=True)

            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            trackResult = track.track(sYear, sMonth, sDay, sHour, eHour, sites, now)
            if trackResult:
                return render_to_response("DataProc/suc.html", {},context_instance=RequestContext(request))
            else:
                return render_to_response("DataProc/fail.html", {},context_instance=RequestContext(request))
    return render_to_response("DataProc/track.html", {'form': form},context_instance=RequestContext(request))


class trackRTThread(threading.Thread): #The timer class is derived from the class threading.Thread
    #dst.ext有问题

    def __init__(self, threadname, dst, ext):
        threading.Thread.__init__(self)
        self.dst_station = dst
        self.ext_station = ext
        self.name        = threadname
        self.thread_stop = False

    def run(self): #Overwrite run() method, put what you want the thread do here
        trackrt.trackrt(self.dst_station, self.ext_station)

    def stop(self):
        self.thread_stop = True


def killTrackRT(request):
    trackRT_ID = request.GET['trackRT_ID']
    call('kill %s' % trackRT_ID, shell=True)
    request.session['trackRT_ID'].remove(trackRT_ID)
    log.info("kill ", trackRT_ID)
    return HttpResponse("sucess!")


def trackRTProcess(request):
    global tasksNum, tasks
    tasksNum += 1   #需设定上限
    #if thread != None:
    #    thread == None
    des_station = data['des_station']
    extra_station = data['extra_station']
    csv_time = data['time']

    #thread = trackRTThread('1',des_station,extra_station)
    #thread.setDaemon(False)
    #thread.start()

    log.info('trackRTProcess')
    #==================================
    threadname = "thread_%s" % tasksNum
    log.info('======================current running thread', threadname)
    task = trackRTThread(threadname, des_station, extra_station)
    task.setDaemon(False)
    task.start()
    time.sleep(2)    #  给trackRT生成数据留一些缓冲时间
    pid = os.popen('pgrep trackRT').readlines()
    log.info("========pid======", pid)
    tasks.append(task)

    #==================================
    request.session['trackRT_ID'] = pid
    '''if len(request.session['trackRT_ID'])!=0:
        request.session['trackRT_ID'].append(str(pid))
    else:
        request.session['trackRT_ID'] = []
        request.session['trackRT_ID'].append(str(pid))'''
    log.info('***********', request.session['trackRT_ID'])
    return HttpResponse("sucess!")

@login_required()
def trackProcess(request):
    sYear = (int)(request.GET['sYear'])
    sMonth = (int)(request.GET['sMonth'])
    sDay = (int)(request.GET['sDay'])
    sHour = (int)(request.GET['sHour'])
    eHour = (int)(request.GET['eHour'])
    log.info(sYear, sMonth, sDay, sHour, eHour)
    sites = request.GET['sites'].split()
    log.info(sites)

    #下载一天的sp3数据
    days = monthToDay.ymdToYd(sYear, sMonth, sDay)
    filedir = os.path.join(cwd, 'track/track_data')
    cmd = "cd %s;csh %s/get_orbits -archive sopac -yr %s -doy %s -ndays 1" % (filedir, cwd, sYear, days)
    call(cmd, shell=True)

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    trackResult = track.track(sYear, sMonth, sDay, sHour, eHour, sites, now)
    if trackResult:
        return HttpResponse(trackResult)
    else:
        return render_to_response("png_track.html",
                {'png': '/track/track_picture/track%s.png' % now, 'file': '/track/log/CGDM056a.NEU.somt.LC'})


def trackRTView(request):
    time.sleep(3)    #  给trackRT生成数据留一些缓冲时间
    trackRT_ID = int(request.session['trackRT_ID'][-1])
    log.info(trackRT_ID)
    return render_to_response('trackRTView.html', {'trackRT_ID': trackRT_ID},context_instance= RequestContext(request))

@login_required()
def datatrackrt(request):
    form = TrackRTForm()
    user = request.user.username
    if request.method=="POST":
        form = TrackRTForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            des_station = data['des_station']
            extra_station = data['extra_station']
            csv_time = data['time']


            log.info('trackRTProcess')
            #==================================
            threadname = "thread_%s" % tasksNum
            log.info('======================current running thread', threadname)
            task = trackRTThread(threadname, des_station, extra_station)
            task.setDaemon(False)
            task.start()
            time.sleep(2)    #  给trackRT生成数据留一些缓冲时间
            pid = os.popen('pgrep trackRT').readlines()
            log.info("========pid======", pid)
            tasks.append(task)

            #==================================
            request.session['trackRT_ID'] = pid
            '''if len(request.session['trackRT_ID'])!=0:
                request.session['trackRT_ID'].append(str(pid))
            else:
                request.session['trackRT_ID'] = []
                request.session['trackRT_ID'].append(str(pid))'''
            log.info('***********', request.session['trackRT_ID'])
            return HttpResponseRedirect('DataProc/trackRT_View?des_site="+des_Station+"&ext_site="+ext_Station+"&csv_time="+csv_Time')
    return render_to_response("DataProc/trackrt.html", {'form': form},context_instance=RequestContext(request))

# @login_required()
# def atmosphericDelay(request):
#     form= ProcessForm()
#     return render_to_response("atmosphericDelay.html", {'form': form},context_instance=RequestContext(request))

# @login_required()
# def baseline(request):
#     form = ProcessForm()
#     return render_to_response("baseline.html", {'form': form},context_instance=RequestContext(request))


@login_required()
def highFrequencyData(request):
    return render_to_response("highFrequencyData.html", {},context_instance=RequestContext(request))

def readDst(prj):
    dst=[]
    f = prj + "/tables/sites.defualts"
    line = linecache.getlines(f)
    for l in xrange(32, len(line) + 1):
        dst.append(l.split()[0])
    return dst

@login_required()
def baselineProcess(request):
    error = ""
    username = request.user.username
    form =ProcessForm()
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year_1, day_1, year_2, day_2 = int(data['StartYear']), int(data['StartDay']), int(data['EndYear']), int(data['EndDay'])
            extractOscalaFile.extractTempFile(year_1, day_1, year_2, day_2, 'baseline',username)
            getBaselineData.getData('baseline',username)
            if not error:
                return render_to_response("DataProc/suc.html", {},context_instance=RequestContext(request))
            else:
                return render_to_response("DataProc/fail.html", {},context_instance=RequestContext(request))
    return render_to_response("DataProc/baseline.html", {'form': form},context_instance=RequestContext(request))

@login_required()
def atmosphereProcess(request):
    username = request.user.username
    error = ""
    form = ProcessForm()
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year_1, day_1, year_2, day_2 = int(data['StartYear']), int(data['StartDay']), int(
                data['EndYear']), int(data['EndDay'])
            extractOscalaFile.extractTempFile(year_1, day_1, year_2, day_2, 'atmosphere')
            getAtmosphereData.getData('atmosphere',username)
            if not error:
                return render_to_response("DataProc/suc.html", {},context_instance=RequestContext(request))
            else:
                return render_to_response("DataProc/fail.html", {},context_instance=RequestContext(request))
    return render_to_response("DataProc/atmosphere.html", {'form': form},context_instance=RequestContext(request))


@login_required()
def bulkProcess(request,StartYear,StartDay,EndYear,EndDay,IGS):
    error = ''
    username = request.user.username
    year_1, day_1, year_2, day_2, IGS = int(StartYear), int(StartDay), int(
        EndYear), int(EndDay), IGS
    os.chdir(SOFTWAREPATH)
    if not os.path.exists(username):
        Init_experiment(username, year_1, year_2)
    error += Gamitdata_analysing(username, year_1, day_1, year_2, day_2, IGS)
    error += ts_process(username)
    getMbData.getMbData(dst)
    error += vel_process(username)
    extractOscalaFile.extractFile(year_1, day_1, year_2, day_2)
    getBaselineData.getData('batch')
    getAtmosphereData.getData('batch')
    error = error if error else "successful"
    return HttpResponse(error)

@login_required()
def writeConfigFile(request):
    if 'editConfig' in request.GET:
        configText = request.GET['editConfig']
        log.info(configText)
        modifyText.writeContentToEnd(configText)
    else:
        log.info('error write')
    pre = request.META['HTTP_REFERER']
    return HttpResponseRedirect(pre)
    #checkUser(request)
    #return render_to_response("dataProcessing.html",{'username':username,'error':error,'refStation':'jplm'})

@login_required()
def modifyConfigFile(request):
    modifyType = request.POST['modifyType']
    if modifyType == 'read':
        log.info(modifyType)
        configContent = modifyText.getContentFromEnd()
        return HttpResponse(configContent)
    elif modifyType == 'write':
        configText = request.POST['configText']
        modifyText.writeContentToEnd(configText)
        return HttpResponse('successful')
    elif modifyType == 'backup':
        modifyText.backupFile()
        return HttpResponse('successful')
    elif modifyType == 'reset':
        modifyText.reset()
        return HttpResponse('successful')
    elif modifyType == 'restore':
        modifyText.restore()
        return HttpResponse('successful')

def Init_experiment(prj, year_1, year_2):
#   清理experiment文件，根据初始年日及最终年日生成对应文件夹存放结果，同时将tables里必需的文件链入年份内的tables文件里
    global error
    log.info('init_experiment' + prj)
    os.mkdir(prj)
    os.popen("cd %s;mkdir experiment" % prj)
    os.chdir(SOFTWAREPATH + prj+"/experiment")
    for year in xrange(year_1, year_2 + 1):
        os.popen("mkdir %s;cd %s; mkdir rinex; ln -s %s/????/* rinex; cp -rf %s ../tables/ " % (
        str(year), str(year), RINEXPATH, GAMITTABLE))
    return True

@login_required()
def Gamitdata_analysing(prj, year_1, day_1, year_2, day_2, IGS):
    error = ''
    log.info('analysing')
    os.chdir(SOFTWAREPATH + prj)
    for t in xrange(year_1, year_2 + 1):
        outfiles0 = commands.getstatusoutput('cd experiment/%s ; sh_setup -yr %d' % (str(t), t))
        log.info(outfiles0)
        try:
            if  year_2 - year_1 == 0:
                cmd_gamit = 'cd experiment/%s ; sh_gamit -expt scal -s %d %d %d -orbit %s -copt x k p -dopts c ao > sh_gamit.log' % (
                str(t), t, day_1, day_2, IGS)
                cmd_glred = 'cd experiment/%s ; sh_glred -s %d %d %d %d -expt scal -opt H G E > sh_glred.log' % (
                str(t), t, day_1, t, day_2)  #----------------bxy 2012-1-5)
                os.popen(cmd_gamit)
                os.popen(cmd_glred)
                os.popen(
                    'cp ' + os.path.join(SOFTWAREPATH + prj, 'experiment/%s/glbf/h*glx ' % str(year_1)) + os.path.join(
                        cwd, 'exp2nd/h_results'))
            if  year_2 - year_1 == 1:
                if  t == year_1:
                    sumday = isLeap(year_1)
                    log.info(
                        'cd experiment/%s ; sh_gamit -expt scal -s %d %d %d -orbit %s -copt x k p -dopts c ao > sh_gamit.log' % (
                        str(t), t, day_1, sumday, IGS))

                    outfiles5 = commands.getstatusoutput('cd experiment/%s ; \
                                                sh_gamit -expt scal -s %d %d %d -orbit %s -copt x k p -dopts c ao > sh_gamit.log' % (
                    str(t), t, day_1, sumday, IGS))
                    outfiles12 = commands.getstatusoutput('cd experiment/%s ; \
                                                sh_glred -s %d %d %d %d -expt scal -opt H G E >&! sh_glred.log' % (
                    str(t), t, day_1, t, sumday))
                    outfiles13 = commands.getstatusoutput(
                        'cd experiment/%s ; sh_cleanup -s %d %d %d %d -dopts p x k' % (str(t), t, day_1, t, sumday))
                    os.popen('cp ' + os.path.join(cwd, 'experiment/%s/glbf/h*glx ' % str(year_1)) + os.path.join(cwd,
                                                                                                                 'exp2nd/h_results'))
                else:
                    log.info(
                        'cd experiment/%s ; sh_gamit -expt scal -s %d 1 %d  -orbit %s -copt x k p -dopts c ao> sh_gamit.log' % (
                        str(t), t, day_2, IGS))
                    outfiles6 = commands.getstatusoutput('cd experiment/%s ; \
                                                sh_gamit -expt scal -s %d 1 %d  -orbit %s -copt x k p -dopts c ao> sh_gamit.log' % (
                    str(t), t, day_2, IGS))
                    outfiles = commands.getstatusoutput('cd experiment/%s ; \
                                                sh_glred -s %d 1 %d %d -expt scal -opt H G E >&! sh_glred.log' % (
                    str(t), t, t, day_2))
                    outfiles = commands.getstatusoutput(
                        'cd experiment/%s ; sh_cleanup -s %d 1 %d %d-dopts p x k' % (str(t), t, t, day_2))
                    os.popen('cp ' + os.path.join(cwd, 'experiment/%s/glbf/h*glx ' % str(year_2)) + os.path.join(cwd,
                                                                                                                 'exp2nd/h_results'))

            if  year_2 - year_1 > 1:
                if  t == year_1:
                    sumday = isLeap(t)
                    outfiles7 = commands.getstatusoutput('cd experiment/%s ; \
                                                sh_gamit -expt scal -s %d %d %d  -orbit %s -copt x k p -dopts c ao> sh_gamit.log' % (
                    str(t), t, day_1, sumday, IGS))
                    outfiles = commands.getstatusoutput('cd experiment/%s ; \
                                                sh_glred -s %d %d %d %d -expt scal -opt H G E >&! sh_glred.log' % (
                    str(t), t, day_1, t, sumday))
                    outfiles = commands.getstatusoutput(
                        'cd experiment/%s ; sh_cleanup -s %d %d %d %d -dopts p x k' % (str(t), t, day_1, t, sumday))
                    os.popen('cp ' + os.path.join(cwd, 'experiment/%s/glbf/h*glx ' % str(year_1)) + os.path.join(cwd,
                                                                                                                 'exp2nd/h_results'))
                if  t == year_2:
                    outfiles8 = commands.getstatusoutput('cd experiment/%s ; \
                                                sh_gamit -expt scal -s %d 1 %d  -orbit %s -copt x k p -dopts c ao> sh_gamit.log' % (
                    str(t), t, day_2, IGS))
                    outfiles = commands.getstatusoutput('cd experiment/%s ; \
                                                sh_glred -s %d 1 %d %d -expt scal -opt H G E >&! sh_glred.log' % (
                    str(t), t, t, day_2))
                    outfiles = commands.getstatusoutput(
                        'cd experiment/%s ; sh_cleanup -s %d 1 %d %d-dopts p x k' % (str(t), t, t, day_2))
                    os.popen('cp ' + os.path.join(cwd, 'experiment/%s/glbf/h*glx ' % str(year_2)) + os.path.join(cwd,
                                                                                                                 'exp2nd/h_results'))
                if  t != year_1 and t != year_2:
                    sumday = isLeap(year_2 - 1)

                    log.info(
                        'cd experiment/%s ; sh_gamit -expt scal -s %d 1 %d %d  -orbit %s -copt x k p -dopts c ao> sh_gamit.log' % (
                        str(t), t, t, sumday, IGS))
                    outfiles9 = commands.getstatusoutput('cd experiment/%s ; \
                                                    sh_gamit -expt scal -s %d 1 %d %d  -orbit %s -copt x k p -dopts c ao> sh_gamit.log' % (
                    str(t), t, t, sumday, IGS))
                    outfiles = commands.getstatusoutput('cd experiment/%s ; \
                                                    sh_glred -s %d 1 %d %d -expt scal -opt H G E >&! sh_glred.log' % (
                    str(t), t, t, sumday))
                    outfiles = commands.getstatusoutput(
                        'cd experiment/%s ; sh_cleanup -s %d 1 %d %d -dopts p x k' % (str(t), t, t, sumday))
                    os.popen('cp ' + os.path.join(cwd, 'experiment/%s/glbf/h*glx ' % str(t)) + os.path.join(cwd,
                                                                                                            'exp2nd/h_results'))
        except Exception:
            error += "%s: Error occured when processing by command sh_gamit , sh_glred or sh_cleanup.\n" % datetime.datetime.now()
            log.info(
                "%s: Error occured when processing by command sh_gamit , sh_glred or sh_cleanup.\n" % datetime.datetime.now())
    return error

@login_required()
def ts_process(prj):
    error = ''
    log.info('ts_process')
    #   用Gamitdata_analysing()里处理出的数据画时间序列和速度场
    #   vsoln文件夹里存放结果文件和生成的图片
    os.chdir(SOFTWAREPATH + prj)
    #   结果处理，由sh_plotcrd得到时间序列结果
    #   sh_plotcrd 参数中-s long控制横坐标的跨度大，默认default为short，跨度小，-mb生成mb文件，从中提取结果
    try:
        os.popen('cd experiment/vsoln ;                                                             \
        ls ../????/glbf/h*glx > scal.gdl ;                                                          \
        glred 6 globk_comb.prt globk_comb.log scal.gdl globk_comb.cmd ;                             \
        sh_plotcrd -f globk_comb.org -s long -res -o 1 -vert -col 1 -mb;                               \
        globk 6 globk_vel.prt globk_vel.log scal.gdl globk_vel.cmd ;                                \
        sh_plotvel -ps scal -f globk_vel.org -R240/246/32/35 -factor 0.5 -arrow_value 10  -page L ')
    except Exception:
        error = "%s: Processing by command sh_plotcrd or sh_plotvel wrong!\n" % datetime.datetime.now()
        log.error("Processing by command sh_plotcrd or sh_plotvel wrong!")
    return error

@login_required()
def vel_process(prj):
    error = ''
    os.chdir(SOFTWAREPATH + prj)
    orgVelPath = os.path.join(SOFTWAREPATH + prj, 'experiment/vsoln/globk_vel.org')
    desVelPath = os.path.join(SOFTWAREPATH + prj, 'exp2nd/vel_result/globk_vel.org')
    cmd = 'cp %s %s' % (orgVelPath, desVelPath)
    try:
        os.popen(cmd)
        cmd = 'cd %s ; ./velDataCollect.sh' % os.path.join(SOFTWAREPATH + prj, 'exp2nd/vel_result')
        os.popen(cmd)
    except Exception:
        error = "%s: Processing by command velDataCollect.sh wrong!\n" % datetime.datetime.now()
        log.error("%s: Processing by command velDataCollect.sh wrong!\n" % datetime.datetime.now())
    return error

def tableStatistic(username):
    os.chdir(SOFTWAREPATH + username + "/experiment/tables")
    #"soltab.*","luntab.*","nutabl.*",
    filestatus = [{'name': filen, 'time': time.ctime(os.path.getmtime(filen))} for filen in fileList]
    return filestatus

@login_required()
def tableStatisticDetail(request, filename):
    result = ""
    if filename == "bulk":
        os.popen("cd %s" % GAMITTABLE)
        [os.popen("mv %s %s.bak;wget -o %s.log ftp://garner.ucsd.edu//archive/garner/gamit/tables/%s" % (
        files, files, files, files)) for files in fileList]
        os.chdir(SOFTWAREPATH + username + "/tables/")
        [os.popen("mv %s %s.bak;wget -o %s.log ftp://garner.ucsd.edu//archive/garner/gamit/tables/%s" % (
        files, files, files, files)) for files in fileList]
        for filen in fileList:
            result += readFile(GAMITTABLE + filen + ".log")
    elif filename in fileList:
        os.popen("cd %s ;mv %s %s.bak;wget -o %s.log ftp://garner.ucsd.edu//archive/garner/gamit/tables/%s" % (
        GAMITTABLE, filename, filename, filename, filename))
        os.chdir(SOFTWAREPATH + username + "/tables/")
        os.popen("mv %s %s.bak;wget -o %s.log ftp://garner.ucsd.edu//archive/garner/gamit/tables/%s" % (
        filename, filename, filename, filename))
        result += readFile(GAMITTABLE + filename + ".log")
    else:
        result = "error"
    return HttpResponse(result)

@login_required()
def dataStatisticDetail(request):
    usern = username.username
    os.chdir(SOFTWAREPATH + usern + "/experiment/")
    os.path.exists("rinex") and True or os.mkdir("rinex")
    os.popen("ln -s %s/????/* rinex;" % RINEXPATH)
    form = BulkProcessForm()
    if request.method == 'POST':
        form = BulkProcessForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            year_1, day_1, year_2, day_2,IGS = int(data['StartYear']), int(data['StartDay']), int(data['EndYear']), int(data['EndDay']),data['IGS']
        else:
            fileStatus = tableStatistic(user)
            return render_to_response('DataProcDataProc.html',{'form':form,'fileStatus':fileStatus,'fileList':fileList})
    siteList = config.get("path", "checklist").split('%%')
    years = [str(year)[:2] for year in xrange(year_1, year_2 + 1)]
    if len(years) == 1:
        days = [('%03d' % day, years[0]) for day in xrange(day_1, day_2 + 1)]
    if len(years) > 1:
        common_years = [years[i] for i in xrange(1, len(years) - 1)]
        days = [('%03d' % day, years[0]) for day in xrange(day_1, isLeap(int(years[0]) + 2000) + 1)]
        days += [('%03d' % day, year) for year in common_years for day in xrange(1, isLeap(int(year) + 2000) + 1)]
        days += [('%03d' % day, years[len(years) - 1]) for day in xrange(1, day_2 + 1)]
    for site in siteList:
        os.chdir(SOFTWAREPATH + userm + "/experiment/rinex/")
        l = commands.getoutput("ls *.*o | grep %s" % site)
        l = [(a[4:7], a[9:11]) for a in l]
        infos = list(set(copy.deepcopy(days)) - set(dates[1]))
        inforarray.append({'site': site, 'info': infos})
    inforarray = []
    return render_to_response("dataStatisticResult.html",
            {'sitelist': siteList, 'infoList': inforarray, 'year_1': year_1,
             'year_2': year_2, 'day_1': day_1, 'day_2': day_2, 'IGS': IGS, 'years': xrange(year_1, year_2 + 1)},context_instance=RequestContext(request))

@login_required()
def configEdit(request):
    return render_to_response("configEdit.html", {'fileList': fileList, 'username': username},context_instance=RequestContext(request))

@login_required()
def configEditDetail(request, filename):
    username = request.user.username
    os.chdir(SOFTWAREPATH + username + "/experiment/tables/")
    print readFile(filename),filename,os.getcwd()
    return HttpResponse(readFile(filename))

@login_required()
def readGamitLog(request, year):
    username = request.user.username
    os.chdir(SOFTWAREPATH + username + "/experiment/%s/" % year)
    f = linecache.getlines("sh_gamit.log")
    return f

@login_required()
def saveConfigFile(request, filename):
    try:
        print request
        username = request.user.username
        configText = request.POST['editConfig']
        i=writeFile(SOFTWAREPATH + username + "/experiment/tables/" + filename,configText)
        print i
        if i:
            return True
    except Exception, e:
        print e
        raise e
    
@login_required()
def resetConfigFile(request):
    username = request.user.username
    os.chdir(SOFTWAREPATH + username + "/tables/")
    [os.popen("rm %s;cp %s.bak %s" % (filename, filename, filename)) for filename in fileList]
    return true

def s_result(request):
    sitelist=readDst()
    key=request.POST['key']
    rs=[]
    for sitecode in sitelist:
        kmp_rs=kmp.kmp_matcher(sitecode,key)
        if kmp_rs!=-1:
            rs.append(sitecode)
    return HttpResponse(simplejson.dumps(rs))

@login_required()
def DataProc(request):
    user = request.user.username
    print request.user
    os.chdir(CONFIG.SOFTWAREPATH)
    if not os.path.exists(user):
        Init_experiment(user,2012,2012)
    form = BulkProcessForm()
    fileStatus = tableStatistic(user)
    return render_to_response('DataProc/DataProc.html',{'form':form,'fileStatus':fileStatus,'fileList':fileList},context_instance=RequestContext(request))