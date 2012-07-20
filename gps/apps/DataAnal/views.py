#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import atan,sqrt,cos,sin
import os,linecache,datetime
#from sitesInfo import readInfo
from gps.utils import ymdToYd,isLeap
import commands
from django.shortcuts import render_to_response
#import getMax_Min
from django.utils.log import logging
#import customforms
from django.contrib.auth.decorators import user_passes_test
from gps.config import CONFIG
from django.template import RequestContext
#cwd=os.getcwd()
log = logging.getLogger('django')

@user_passes_test(lambda u:u.is_authenticated)
def strain(request):
    user = request.user.username
    velFilePath = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/vel_result/result.vel')
    strainFilePath = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/strain_result/NCCGPS.dat')
    cmd = 'cp %s %s' % (velFilePath,strainFilePath)
    try:
        os.popen(cmd)
        cmd='cd %s ; ./strain  ; ./drawstrain.sh ' % (os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/strain_result'))
        os.popen(cmd)        
    except Exception:
        error = "Strain Processing by command strain wrong!"
        log.exception(error)
    return render_to_response("DataAnal/strain.html",{'file':CONFIG.SOFTWAREPATH+user+'/exp2nd/strain_result/NCCGPS.dat','png':CONFIG.SOFTWAREPATH+user+'/exp2nd/strain_result/strain.png'},context_instance=RequestContext(request))
        
#读取站点数目
#sitelist=readInfo(0)
#citenum=len(sitelist)
#citenum表示站点数目 num表示baseline行数

def doubleSite(siteA,siteB):  
    if siteA<=siteB:
        doublesite=siteA.upper()+'_'+siteB.upper()
    else:
        doublesite=siteB.upper()+'_'+siteA.upper()
    return doublesite

@user_passes_test(lambda u:u.is_authenticated)
def expandrate(request):
    return render_to_response('DataAnal/expandrate.html',{},context_instance=RequestContext(request))

@user_passes_test(lambda u:u.is_authenticated)    
def expandrateAnalyse(request):
    
    site1 = request.POST.get("site1")
    site2 = request.POST.get("site2")
    site3 = request.POST.get("site3")
   
    #生成两两组合格式的站点组合并存入circle列表中
    circle= [doubleSite(site1, site2), doubleSite(site1, site3), doubleSite(site2, site3)]


    #获取baseline.dat中的数据
    user = request.user.username
    baselinefile = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/baseline_batch/baseline.dat')

    from gps.utils import readFile
    lines = readFile(baselinefile)
    #从得到的列表中获取所需要的数据
    ls = [l.split() for l in lines]
    distance = [[l[1][:8],l[15],l[0]] for l in ls if l[0] in circle]  #l[15]为L的值
    length=len(distance)
    #正常情况值应为3
    
    
    a = [eval(distance[i][0]) for i in range(length) if i%3 == 0]
    b = [eval(distance[i][0]) for i in range(length) if i%3 == 1]
    c = [eval(distance[i][0]) for i in range(length) if i%3 == 2]
    p = [(a[i]+b[i]+c[i])/2 for i in range(length/3)]
    s = [[distance[3*i][0],sqrt(p[i]*(p[i]-a[i])*(p[i]-b[i])*(p[i]-c[i]))] for i in range(length/3)]

    #!!!!!!!!!!!!!!!!!!!!!未判断文件夹是否存在，因此该文件夹应提前准备好
    #将数据写入文件
    expandratefile = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/expandrate_result/expandrate.dat')
    ff = open(expandratefile,"w")
    #baseX = s[0][0]
    baseY = s[0][1]
    for ss in s:
        #ss[0] = ss[0]-baseX
        ss[1] = ss[1]-baseY
        format ="%0.4f" % ss[1]
        line = str(ss[0])+" "+format+" "+"0"+'\n'
        ff.writelines(line)
    ff.close()
    
    scope = getMax_Min.getMax_MinFromFile(expandratefile,[1,2])
    x_scope = scope[0].split()
    y_scope = scope[1].split()
    
    maxX = "%d" % (float(x_scope[0]) + 1)  
    minX = "%d" % (float(x_scope[1]))
    maxY = "%d" % (abs(float(y_scope[0])))
    maxY = "%d" % (float(y_scope[0]) + 10**(len(maxY)-1))
    minY = "%d" % (abs(float(y_scope[1])))
    minY = "%d" % (float(y_scope[1]) - 10**(len(minY)-1))
    
    disY = float(maxY)/5.0
    
    #画出图像 纵坐标有问题？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
    imagename = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/expandrate_result/expandrate.pdf')
    
    cmd = 'psxy %s -JX6.5/2.0 -R%s/%s/%s/%s -Ba0.5f0.1:"":/a%0.2ff5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i > %s' % (expandratefile,minX,maxX,minY,maxY,disY,imagename)
    
    commands.getstatusoutput(cmd)
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    png = 'exp2nd/expandrate_result/%sexpandrate%s.png' %(user,now)
    subprocess.call('cp %s %s'%(CONFIG.SOFTWAREPATH+user+'/'+png,CONFIG.SOFTWAREPATH+'static/img/%sexpandrate%s.png'%(user,now)),shell=True)
    os.popen('convert -trim %s %s ; rm %s' % (imagename,os.path.join(CONFIG.SOFTWAREPATH+user,png),imagename)) 
    return render_to_response('/DataProc/png_expandRate.html',{'file':CONFIG.SOFTWAREPATH+user+'/exp2nd/expandrate_result/expandrate.dat','png':CONFIG.SOFTWAREPATH+'static/img/%sexpandrate%s.png'%(user,now)},context_instance=RequestContext(request))
  	
	
def crosssection(request):
    return render_to_response('DataAnal/crosssection.html',{},context_instance=RequestContext(request))
    
def crosssectionAnalyse(request): #num表示线
    user = request.user.username
    num=int(request.GET['num'])-1
    #num=1
    x= [[-1.557911456, 207.016637], [0.6773785407, -56.61408148], [0.9467484395, -87.18706211],
        [1.192860257, -114.5317538], [1.352398629, -131.6030612], [0.5739991985, -40.78014064]]
	#把六个剖面拟合直线的方程加入列表存储,统一为Ax-y+C=0, 第一个参数是A，第二个参数是C




    #求出角度
    theta = atan(x[num][0])
    #(N,E,VN,VE) =(float(0),float(0),float(0),float(0))
	#包含所有本地站点的列表，参数依次为站点名，经度，纬度，经度方向的速度，纬度方向的速度
    #citelist=[['cit1',122.05,36.933,9.4,-5],['wlsn',114.917,40.717,5.2,1.4]]
    
    #读取速度场结果文件来获取站点+经度+纬度+VE+VN
    
    siteinfo = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/vel_result/result.vel')
    #siteinfo = os.path.join(cwd,'exp2nd/vel_result/vel1.result')
    f = open(siteinfo,'r')
    lines = f.readlines()            
    f.close()
    lns = [l.split() for l in lines]
    citelist = [[l[-1][:4],float(l[0]),float(l[1]),float(l[2]),float(l[3])] for l in lns]
    #distance中元素依次为距离、台站名、垂直剖面的速度、平行剖面的速度 
    distance = [[abs(cite[1]*x[num][0]-cite[2]*x[num][1])/sqrt(x[num][0]*x[num][0]+1),cite[0],(cite[4]*cos(theta)+cite[3]*sin(theta)),(cite[4]*sin(theta)-cite[3]*cos(theta))] for cite in citelist]
    distance.sort()
    
    #将数据写入文件
    parallel_filepath = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/crosssection_result/parallel.dat')
    
    ff = open(parallel_filepath,"w")
    maxParallelY = -1
    minParallelY = 1000000
    for d in distance:
        formatX = "%0.4f" % d[0]
        formatY = "%0.4f" % d[3]
        '''
        if d[3]>maxParallelY :
            maxParallelY = d[3]
        if d[3]<minParallelY:
            minParallelY=d[3]
        '''
        line = formatX+" "+formatY+" "+"0"+'\n'
        ff.writelines(line)
    ff.close()
    
    
    scope = getMax_Min.getMax_MinFromFile(parallel_filepath,[1,2])
    x_scope = scope[0].split()
    y_scope = scope[1].split()
    maxX_parallel = "%d" % (abs(float(x_scope[0])))
    maxX_parallel = "%d" % (float(x_scope[0]) + 10**(len(maxX_parallel)-1))
    minX_parallel = "%d" % (abs(float(x_scope[1])))
    minX_parallel = "%d" % (float(x_scope[1]) - 10**(len(minX_parallel)-1))
    maxY_parallel = "%d" % (abs(float(y_scope[0])))
    maxY_parallel = "%d" % (float(y_scope[0]) + 10**(len(maxY_parallel)-1))
    minY_parallel = "%d" % (abs(float(y_scope[1])))
    minY_parallel = "%d" % (float(y_scope[1]) - 10**(len(minY_parallel)-1))
    
    disX_parallel = float(maxX_parallel)/5.0
    disY_parallel = float(maxY_parallel)/5.0
    
    vertical_filepath = os.path.join(CONFIG.SOFTWAREPATH+user,'exp2nd/crosssection_result/vertical.dat')
    
    ff = open(vertical_filepath,"w")
    maxverticalY=-1
    minverticalY=1000000
    for d in distance:
        formatX = "%0.4f" % d[0]
        formatY = "%0.4f" % d[2]
        '''
        if d[2]>maxverticalY :
            maxverticalY=d[2]+1
        if d[2]<minverticalY:
            minverticalY=d[2]
        '''
        line = formatX+" "+formatY+" "+"0"+'\n'
        ff.writelines(line)
    ff.close()
    
    scope = getMax_Min.getMax_MinFromFile(vertical_filepath,[1,2])
    x_scope = scope[0].split()
    y_scope = scope[1].split()
    maxX_vertical = "%d" % (abs(float(x_scope[0])))
    maxX_vertical = "%d" % (float(x_scope[0]) + 10**(len(maxX_vertical)-1))
    minX_vertical = "%d" % (abs(float(x_scope[1])))  #为了算最大值位数
    minX_vertical = "%d" % (float(x_scope[1]) - 10**(len(minX_vertical)-1))
    maxY_vertical = "%d" % (abs(float(y_scope[0])))
    maxY_vertical = "%d" % (float(y_scope[0]) + 10**(len(maxY_vertical)-1))
    minY_vertical = "%d" % (abs(float(y_scope[1])))
    minY_vertical = "%d" % (float(y_scope[1]) - 10**(len(minY_vertical)-1))
    
    disX_vertical = float(maxX_vertical)/3.0
    disY_vertical = float(maxY_vertical)/3.0
    
    files=[]
    pngs=[]
    now=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    parallel = 'exp2nd/crosssection_result/parallel'
    vertical = 'exp2nd/crosssection_result/vertical'
    #==================================绘制水平方向图=====================================
    filename= os.path.join(CONFIG.SOFTWAREPATH+user,parallel)
    imagename = filename+now+'.pdf'
    pngname = filename+now+'.png'
    #print 'psxy %s -JX10/5 -R%d/%d/%d/%d -Ba200f50:"":/a100f25:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i > %s' % (parallel_filepath,int(distance[0][0]),int(distance[-1][0]),int(minParallelY),int(maxParallelY),imagename)
    parallel_cmd = 'psxy %s -JX6.5/2.0 -R%s/%s/%s/%s -Ba%0.2ff5:"":/a%0.2ff5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i > %s' % (parallel_filepath,minX_parallel,maxX_parallel,minY_parallel,maxY_parallel,disX_parallel,disY_parallel,imagename)
    
    log.info('%s' %parallel_cmd)
    
    information = commands.getstatusoutput(parallel_cmd)
    log.info('%s' %str(information))
    os.popen('convert -trim %s %s ; rm %s' % (imagename,pngname,imagename)) 
    files.append('/'+parallel+'.dat')
    pngs.append('/'+parallel+now+'.png')
    
    #==================================绘制垂直方向图=======================================
    
    filename= os.path.join(CONFIG.SOFTWAREPATH+user,vertical)
    imagename = filename+now+'.pdf'
    pngname = filename+now+'.png'
    vertical_cmd = 'psxy %s -JX6.5/2.0 -R%s/%s/%s/%s -Ba%0.2ff5:"":/a%0.2ff5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i > %s' % (vertical_filepath,minX_vertical,maxX_vertical,minY_vertical,maxY_vertical,disX_vertical,disY_vertical,imagename)
    
    log.info('%s' %vertical_cmd)
    
    information = commands.getstatusoutput(vertical_cmd)      
    
    log.info('%s' %str(information))
    os.popen('convert -trim %s %s ; rm %s' % (imagename,pngname,imagename)) 
    files.append('/'+vertical+'.dat')
    pngs.append('/'+vertical+now+'.png')
    
    return render_to_response('/DataProc/png_crosssection.html',{'files':files,'pngs':pngs},context_instance=RequestContext(request))
    
def deltaV(request):
    return render_to_response('/DataProc/deltaV.html',{'png':png},context_instance=RequestContext(request))

def deltaS(request):
    return render_to_response('/DataProc/deltaS.html',{'png':png},context_instance=RequestContext(request))

def drawsomething(year_1,year_2,day_1,day_2):
    return True

