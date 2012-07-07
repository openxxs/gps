#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import atan,sqrt,cos,sin
import os,linecache,datetime
#from sitesInfo import readInfo
from gps.utils import ymdToYd
import commands
from django.shortcuts import render_to_response
import getMax_Min
from django.utils.log import logging
import customforms

cwd=os.path.dirname(__file__)
#cwd=os.getcwd()
log = logging.getLogger('django')

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
    
def strain(request):
    checkUser(request)
    
    velFilePath = os.path.join(cwd,'exp2nd/vel_result/result.vel')
    strainFilePath = os.path.join(cwd,'exp2nd/strain_result/NCCGPS.dat')
    cmd = 'cp %s %s' % (velFilePath,strainFilePath)
    try:
        os.popen(cmd)
        cmd='cd %s ; ./strain  ; ./drawstrain.sh ' % (os.path.join(cwd,'exp2nd/strain_result'))
        os.popen(cmd)        
    except Exception:
        ei  = open(os.path.join(cwd,'info/!exp_errorInfo'),'a')
        ei.write("%s: strain Processing by command strain wrong!\n" % datetime.datetime.now())   
        ei.close()
    return render_to_response("strain.html",{'username':username,'error':error,'file':'/exp2nd/strain_result/NCCGPS.dat','png':'/exp2nd/strain_result/strain.png'})
        
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

def expandrate(request):
    checkUser(request)
    return render_to_response('expandrate.html',{'username':username,'error':error})
    
def expandrateAnalyse(request):
    
    site1 = request.GET['site1']
    site2 = request.GET['site2']
    site3 = request.GET['site3']
    print site1,site2,site3
    
    '''
    site1 = 'JPLM'
    site2 = 'MIZU'
    site3 = 'USUD'
    '''
    
    #生成两两组合格式的站点组合并存入circle列表中
    circle= [doubleSite(site1, site2), doubleSite(site1, site3), doubleSite(site2, site3)]


    #获取baseline.dat中的数据
    
    baselinefile = os.path.join(cwd,'exp2nd/baseline_batch/baseline.dat')
    f = open(baselinefile,'r')
    lines = f.readlines()            
    f.close()
    
    #从得到的列表中获取所需要的数据
    ls = [l.split() for l in lines]
    print "--------------------------------"
    print ls
    distance = [[l[1][:8],l[15],l[0]] for l in ls if l[0] in circle]  #l[15]为L的值
    print distance
    length=len(distance)
    print length                    #正常情况值应为3
    
    
    #疑问：万一数据有问题时，比如某天中有7001_JPLM，7001_WLSN但是没有JPLM_WLSN那样就不能整除3了？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
    a = [eval(distance[i][0]) for i in range(length) if i%3 == 0]
    b = [eval(distance[i][0]) for i in range(length) if i%3 == 1]
    c = [eval(distance[i][0]) for i in range(length) if i%3 == 2]
    p = [(a[i]+b[i]+c[i])/2 for i in range(length/3)]
    s = [[distance[3*i][0],sqrt(p[i]*(p[i]-a[i])*(p[i]-b[i])*(p[i]-c[i]))] for i in range(length/3)]
    #对结果按时间排序并返回
    #s.sort()
    print s
    
    #!!!!!!!!!!!!!!!!!!!!!未判断文件夹是否存在，因此该文件夹应提前准备好
    #将数据写入文件
    expandratefile = os.path.join(cwd,'exp2nd/expandrate_result/expandrate.dat')
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
    print disY
    
    
    #画出图像 纵坐标有问题？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
    imagename = os.path.join(cwd,'exp2nd/expandrate_result/expandrate.pdf')
    
    cmd = 'psxy %s -JX6.5/2.0 -R%s/%s/%s/%s -Ba0.5f0.1:"":/a%0.2ff5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i > %s' % (expandratefile,minX,maxX,minY,maxY,disY,imagename)
    
    print cmd
    
    commands.getstatusoutput(cmd)
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    png = 'exp2nd/expandrate_result/expandrate%s.png' % now
    os.popen('convert -trim %s %s ; rm %s' % (imagename,os.path.join(cwd,png),imagename)) 
    return render_to_response('png_expandRate.html',{'file':'/exp2nd/expandrate_result/expandrate.dat','png':'/'+png})
  	
	
def crosssection(request):
    checkUser(request)
    return render_to_response('crosssection.html',{'username':username,'error':error})
    
def crosssectionAnalyse(request):  #num表示线
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
    
    siteinfo = os.path.join(cwd,'exp2nd/vel_result/result.vel')
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
    parallel_filepath = os.path.join(cwd,'exp2nd/crosssection_result/parallel.dat')
    
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
    print disX_parallel,disY_parallel
    
    
    
    vertical_filepath = os.path.join(cwd,'exp2nd/crosssection_result/vertical.dat')
    
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
    print disX_vertical,disY_vertical
    
    files=[]
    pngs=[]
    now=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    parallel = 'exp2nd/crosssection_result/parallel'
    vertical = 'exp2nd/crosssection_result/vertical'
    #==================================绘制水平方向图=====================================
    filename= os.path.join(cwd,parallel)
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
    
    filename= os.path.join(cwd,vertical)
    imagename = filename+now+'.pdf'
    pngname = filename+now+'.png'
    vertical_cmd = 'psxy %s -JX6.5/2.0 -R%s/%s/%s/%s -Ba%0.2ff5:"":/a%0.2ff5:"":WSen:."": -Ey0.02/2/255/0/0 -Sc0.03 -G255/0/0 -K -P -Y7i > %s' % (vertical_filepath,minX_vertical,maxX_vertical,minY_vertical,maxY_vertical,disX_vertical,disY_vertical,imagename)
    
    log.info('%s' %vertical_cmd)
    
    information = commands.getstatusoutput(vertical_cmd)      
    
    log.info('%s' %str(information))
    os.popen('convert -trim %s %s ; rm %s' % (imagename,pngname,imagename)) 
    files.append('/'+vertical+'.dat')
    pngs.append('/'+vertical+now+'.png')
    
    return render_to_response('png_crosssection.html',{'files':files,'pngs':pngs})

def isLeap(year):
    if (year%4==0 and year%100!=0) or (year%400==0):
        return 366
    else:
        return 365
    
def deltaV(request):
    if request.method == "GET":
	deltaVform = customforms.deltaVForm()
	return render_to_response('deltaV.html',{'form':deltaVform})
    else:
	sy,sd,r = request.POST['startYear'],request.POST['startDay'],request.POST['rate']
	year_1 = int(sy)
	r = int(r)
	year_2 = (int(sd)+5*r) > isLeap(year_1) and (year_1+1) or year_1
	day_1 = int(sd)
	png= []
	print "I am here"
	gamitPath="/home/liu/prj/dependency/gamit10.4/"
	os.popen("rm -f -r experiment")
	os.mkdir("experiment")
	if  year_2-year_1 == 1:        
	    os.popen("cd experiment     ; mkdir %s" % str(year_1))
	    os.popen("cd experiment/%s  ; mkdir tables " % str(year_1))
	    
	    yr_1 = str(year_1)
	    try:
		os.popen('ln -s '+gamitPath+'regional.apr '  +os.path.join(cwd,'experiment/%s/tables/regional.apr' % str(year_1))
		      + ' ; ln -s '+gamitPath+'regional.eq '   +os.path.join(cwd,'experiment/%s/tables/regional.eq' % str(year_1))) 
		      #+' ; ln -s '+gamitPath+'autcln.cmd '    +os.path.join(cwd,'experiment/%s/tables/aucln.cmd' % str(year_1))   
		      #+' ; ln -s '+gamitPath+'eq_rename '     +os.path.join(cwd,'experiment/%s/tables/eq_rename' % str(year_1))) 
	    except Exception:
		error += "%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1))
		log.info("%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1)))
		     
	    os.popen("cd experiment ; mkdir %s" % str(year_2))
	    os.popen("cd experiment/%s ; mkdir tables" % str(year_2))
	    
	    yr_2 = str(year_2)
	    try:
		os.popen('ln -s '+gamitPath+'regional.apr '  +os.path.join(cwd,'experiment/%s/tables/regional.apr' % str(year_2))+ 
		      ' ; ln -s '+gamitPath+'regional.eq '   +os.path.join(cwd,'experiment/%s/tables/regional.eq' % str(year_2)) +
		      ' ; ln -s '+gamitPath+'autcln.cmd '    +os.path.join(cwd,'experiment/%s/tables/aucln.cmd' % str(year_2))   +
		      ' ; ln -s '+gamitPath+'eq_rename '     +os.path.join(cwd,'experiment/%s/tables/eq_rename' % str(year_2))) 
	    except Exception:
		error += "%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1))
		log.info("%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1)))
       
	    
	if  year_2 == year_1:
	    os.popen("cd experiment ; mkdir %s" % str(year_1))
	    os.popen("cd experiment/%s ; mkdir tables" % str(year_1))
	    yr_1 = str(year_1)
	    
	    try:
		os.popen('ln -s '+gamitPath+'regional.apr '  +os.path.join(cwd,'experiment/%s/tables/regional.apr' % str(year_1))+ 
		      ' ; ln -s '+gamitPath+'regional.eq '   +os.path.join(cwd,'experiment/%s/tables/regional.eq' % str(year_1)) +
		      ' ; ln -s '+gamitPath+'autcln.cmd '    +os.path.join(cwd,'experiment/%s/tables/aucln.cmd' % str(year_1))   +
		      ' ; ln -s '+gamitPath+'eq_rename '     +os.path.join(cwd,'experiment/%s/tables/eq_rename' % str(year_1))) 
	    except Exception:
		error += "%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1))
		log.info("%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1)))
		
		
	if  year_2-year_1>1:
	    os.popen("cd experiment ; mkdir %s" % str(year_1))
	    os.popen("cd experiment/%s ; mkdir tables" % str(year_1))
	    yr_1 = str(year_1)
	    try:
		os.popen('ln -s '+gamitPath+'regional.apr '  +os.path.join(cwd,'experiment/%s/tables/regional.apr' % str(year_1))+ 
		      ' ; ln -s '+gamitPath+'regional.eq '   +os.path.join(cwd,'experiment/%s/tables/regional.eq' % str(year_1)) +
		      ' ; ln -s '+gamitPath+'autcln.cmd '    +os.path.join(cwd,'experiment/%s/tables/aucln.cmd' % str(year_1))   +
		      ' ; ln -s '+gamitPath+'eq_rename '     +os.path.join(cwd,'experiment/%s/tables/eq_rename' % str(year_1))) 
	    except Exception:
		error += "%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1))
		log.info("%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1)))
	    os.popen("cd experiment ; mkdir %s" % str(year_2))
	    os.popen("cd experiment/%s ; mkdir tables" % str(year_2))
	    
	    yr_2 = str(year_2)
	    
	    try:
		os.popen('ln -s '+gamitPath+'regional.apr '  +os.path.join(cwd,'experiment/%s/tables/regional.apr' % str(year_2))+ 
		      ' ; ln -s '+gamitPath+'regional.eq '   +os.path.join(cwd,'experiment/%s/tables/regional.eq' % str(year_2)) +
		      ' ; ln -s '+gamitPath+'autcln.cmd '    +os.path.join(cwd,'experiment/%s/tables/aucln.cmd' % str(year_2))   +
		      ' ; ln -s '+gamitPath+'eq_rename '     +os.path.join(cwd,'experiment/%s/tables/eq_rename' % str(year_2))) 
	    except Exception:
		error += "%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1))
		log.info("%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1)))
		
	    for n in range(year_1+1,year_2):
		os.popen("cd experiment ; mkdir %s" % str(n))
		os.popen("cd experiment/%s ; mkdir talbes" % str(n))
		yr_n = str(n)
		try:
		    os.popen('ln -s '+gamitPath+'regional.apr '  +os.path.join(cwd,'experiment/%s/tables/regional.apr' % str(n))+ 
		      ' ; ln -s '+gamitPath+'regional.eq '   +os.path.join(cwd,'experiment/%s/tables/regional.eq' % str(n)) +
		      ' ; ln -s '+gamitPath+'autcln.cmd '    +os.path.join(cwd,'experiment/%s/tables/aucln.cmd' % str(n))   +
		      ' ; ln -s '+gamitPath+'eq_rename '     +os.path.join(cwd,'experiment/%s/tables/eq_rename' % str(n)) +
		      ' ; ln -s data/hfile/*' +os.path.join(cwd,'experiment/glbf/')
		      ) 
		except Exception:
		    error += "%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1))
		    log.info("%s: Linking file from '%s' to 'experiment/%s/tables/' wrong\n" % (datetime.datetime.now(),gamitPath,str(year_1)))
	for i in xrange(1,6):
	    print "i am here"
	    day_2 = day_1 +r
	    if day_2 > isLeap(year_1):
		day_2 -= isLeap(year_1)
		year_2+=1
	    drawsomething(year_1,year_2,day_1,day_2)
	    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	    os.popen("mv exp2nd/vel_result/vel.png exp2nd/vel_result/vel%s.png"%now)
	    png.append("exp2nd/vel_result/vel%s.png"%now)
    print png
    return render_to_response('deltaV.html',{'png':png})

def drawsomething(year_1,year_2,day_1,day_2):
    for t in range(year_1,year_2+1):
	data_path=os.path.join(cwd,'experiment/%s' % str(t))
	data_path1  = os.path.join(data_path,'tables')            
	try:
	    outfiles1   = commands.getstatusoutput('cd experiment/%s/tables ; sh_upd_stnfo -l sd' % str(t))
	    commands.getstatusoutput('cd experiment/%s/tables ; rm %s' % (str(t) , os.path.join(data_path1,'station.info')))
	    cmd = 'cd experiment/%s/tables ; mv %s %s' % (str(t),os.path.join(data_path1,'station.info.new'),os.path.join(data_path1,'station.info'))
	    log.info(cmd)
	    outfiles2 = commands.getstatusoutput(cmd)
	    cmd = 'cd experiment/%s/tables ; sh_upd_stnfo -files ../rinex/*.%so' % (str(t),str(t)[2:])
	    outfiles3 = commands.getstatusoutput(cmd)
	    if  year_2-year_1 == 0:
		#cmd_gamit = 'cd experiment/%s ; sh_gamit -expt scal -s %d %d %d -pres ELEV -orbit %s -copt x k p -dopts c ao > sh_gamit.log' % (str(t),t,day_1,day_2,IGS)
		#log.info('sh_gamit\n',cmd_gamit)
		#outinfo4   = commands.getstatusoutput(cmd_gamit)
		
		#cmd_glred = 'cd experiment/%s ; sh_glred -s %d %d %d %d -expt scal -opt H G E > sh_glred.log' % (str(t),t,day_1,t,day_2)
		cmd_glred = 'cd experiment/%s ; sh_glred -s %d %d %d %d -expt scal -opt H G E > sh_glred.log' % (str(t),t,day_1,t,day_2)  #----------------bxy 2012-1-5
		outfiles11  = commands.getstatusoutput(cmd_glred)
		log.info('sh_glred\n',cmd_glred)         
		#os.popen('cp '+os.path.join(cwd,'experiment/%s/glbf/h*glx ' % str(year_1))+os.path.join(cwd,'exp2nd/h_results'))
		
	    
	    if  year_2-year_1 == 1:
		if  t == year_1:
		    sumday = isLeap(year_1)
		    
		    #log.info('cd experiment/%s ; sh_gamit -expt scal -s %d %d %d -pres ELEV -orbit %s -copt x k p -dopts c ao' % (str(t),t,day_1,sumday,IGS))
		    
		    #outfiles5   = commands.getstatusoutput('cd experiment/%s ; \
						#sh_gamit -expt scal -s %d %d %d -pres ELEV -orbit %s -copt x k p -dopts c ao' % (str(t),t,day_1,sumday,IGS))
		    outfiles12  = commands.getstatusoutput('cd experiment/%s ; \
						sh_glred -s %d %d %d %d -expt scal -opt H G E >&! sh_glred.log' % (str(t),t,day_1,t,sumday))
		    outfiles13  = commands.getstatusoutput('cd experiment/%s ; sh_cleanup -s %d %d %d %d -dopts p x k' % (str(t),t,day_1,t,sumday))
		    #os.popen('cp '+os.path.join(cwd,'experiment/%s/glbf/h*glx ' % str(year_1))+os.path.join(cwd,'exp2nd/h_results'))
		else:
		    #log.info('cd experiment/%s ; sh_gamit -expt scal -s %d 1 %d -pres ELEV -orbit %s -copt x k p -dopts c ao' % (str(t),t,day_2,IGS))
		    #outfiles6   = commands.getstatusoutput('cd experiment/%s ; \
		    #			    sh_gamit -expt scal -s %d 1 %d -pres ELEV -orbit %s -copt x k p -dopts c ao' % (str(t),t,day_2,IGS))
		    outfiles    = commands.getstatusoutput('cd experiment/%s ; \
						sh_glred -s %d 1 %d %d -expt scal -opt H G E >&! sh_glred.log' % (str(t),t,t,day_2))
		    outfiles    = commands.getstatusoutput('cd experiment/%s ; sh_cleanup -s %d 1 %d %d-dopts p x k' % (str(t),t,t,day_2))
		    #os.popen('cp '+os.path.join(cwd,'experiment/%s/glbf/h*glx ' % str(year_2))+os.path.join(cwd,'exp2nd/h_results'))
       
	    if  year_2-year_1 > 1:
		if  t == year_1:
		    sumday = isLeap(t)
		    #outfiles7   = commands.getstatusoutput('cd experiment/%s ; \
		    #			    sh_gamit -expt scal -s %d %d %d -pres ELEV -orbit %s -copt x k p -dopts c ao' % (str(t),t,day_1,sumday,IGS))
		    outfiles    = commands.getstatusoutput('cd experiment/%s ; \
						sh_glred -s %d %d %d %d -expt scal -opt H G E >&! sh_glred.log' % (str(t),t,day_1,t,sumday))
		    outfiles    = commands.getstatusoutput('cd experiment/%s ; sh_cleanup -s %d %d %d %d -dopts p x k' % (str(t),t,day_1,t,sumday))
		    #os.popen('cp '+os.path.join(cwd,'experiment/%s/glbf/h*glx ' % str(year_1))+os.path.join(cwd,'exp2nd/h_results'))
		if  t == year_2:
		    #outfiles8   = commands.getstatusoutput('cd experiment/%s ; \
		    #			    sh_gamit -expt scal -s %d 1 %d -pres ELEV -orbit %s -copt x k p -dopts c ao' % (str(t),t,day_2,IGS))
		    outfiles    = commands.getstatusoutput('cd experiment/%s ; \
						sh_glred -s %d 1 %d %d -expt scal -opt H G E >&! sh_glred.log' % (str(t),t,t,day_2))
		    outfiles    = commands.getstatusoutput('cd experiment/%s ; sh_cleanup -s %d 1 %d %d-dopts p x k' % (str(t),t,t,day_2))
		    #os.popen('cp '+os.path.join(cwd,'experiment/%s/glbf/h*glx ' % str(year_2))+os.path.join(cwd,'exp2nd/h_results'))
		if  t != year_1 and t != year_2:
		    
		    sumday = isLeap(year_2-1)
		    
		    #log.info('cd experiment/%s ; sh_gamit -expt scal -s %d 1 %d %d -pres ELEV -orbit %s -copt x k p -dopts c ao' % (str(t),t,t,sumday,IGS))
		    #outfiles9   = commands.getstatusoutput('cd experiment/%s ; \
		    #				sh_gamit -expt scal -s %d 1 %d %d -pres ELEV -orbit %s -copt x k p -dopts c ao' % (str(t),t,t,sumday,IGS))
		    outfiles    = commands.getstatusoutput('cd experiment/%s ; \
						    sh_glred -s %d 1 %d %d -expt scal -opt H G E >&! sh_glred.log' % (str(t),t,t,sumday))
		    outfiles    = commands.getstatusoutput('cd experiment/%s ; sh_cleanup -s %d 1 %d %d -dopts p x k' % (str(t),t,t,sumday))
		    #os.popen('cp '+os.path.join(cwd,'experiment/%s/glbf/h*glx ' % str(t))+os.path.join(cwd,'exp2nd/h_results'))
		    
	except Exception:
	    error += "%s: Error occured when processing by command sh_gamit , sh_glred or sh_cleanup.\n" % datetime.datetime.now()
	    log.info("%s: Error occured when processing by command sh_gamit , sh_glred or sh_cleanup.\n" % datetime.datetime.now())   
	    
    orgVelPath = os.path.join(cwd,'experiment/vsoln/globk_vel.org')
    desVelPath = os.path.join(cwd,'exp2nd/vel_result/globk_vel.org')
    cmd='cp %s %s' % (orgVelPath,desVelPath)
    try:
	#os.popen(cmd)
    	cmd='cd %s ; ./velDataCollect.sh' % os.path.join(cwd,'exp2nd/vel_result')
	#os.popen(cmd)
    except Exception:
	error += "%s: Processing by command velDataCollect.sh wrong!\n" % datetime.datetime.now()    
	    
    os.popen('cd %s ; cp -f ../result.vel . ; ./draw.sh ;  cp -f  vel.png ../vel.png ; ' % os.path.join(cwd,'exp2nd/vel_result/draw'))
    print cwd  
    return True

if __name__ == '__main__':
    #crosssectionAnalyse(1)
    #expandrateAnalyse("7001","wlsn","jplm")
    #expandrate(0,3)
    expandrateAnalyse(0)# Create your views here.
