from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login,logout
import changeFrame
import myDoy
import  dataDownload 
import os

username=''
error=''

#cwd=os.path.dirname(__file__) 
cwd=os.getcwd()

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
    
def doy(request):
    checkUser(request)
    return render_to_response("doy.html",{'username':username,'error':error})
    
def isDigit(org):
    return ''.join(org.split()).isdigit()
    
def transformDoy(request):
    dateYear = request.GET['dateYear']
    dateMonth = request.GET['dateMonth']
    dateDay = request.GET['dateDay']
    doyYear = request.GET['doyYear']
    doyDay = request.GET['doyDay']
    doyResult=[]
    gpsWeek=''
    decimalYear=''

    if(isDigit(dateYear) and isDigit(dateMonth) and isDigit(dateDay)):      
        doyResult =myDoy.doy([dateYear,dateMonth,dateDay])
        doyYear = dateYear
    elif(isDigit(doyYear) and isDigit(doyDay)):
        doyResult = myDoy.doy([doyYear,doyDay])
        
    elif(isDigit(dateYear) or isDigit(dateMonth) or isDigit(dateDay)):
        if(not isDigit(dateYear)):
            dateYear='2000'
            doyYear='2000'
        if(not isDigit(dateMonth)):
            dateMonth='1'
        if(not isDigit(dateDay)):
            dateDay='1'
        doyResult =myDoy.doy([dateYear,dateMonth,dateDay])

    elif(isDigit(doyYear) or isDigit(doyDay)):
        if(not isDigit(doyYear)):
            doyYear='2000'
        if(not isDigit(doyDay)):
            doyDay='1'
        doyResult = myDoy.doy([doyYear,doyDay])
    else:
        doyResult =myDoy.doy(['2000','1','1'])
        doyYear='2000'
        
    date=doyResult[0].split()
    dateTmp = date[0].split('/')
    dateYear = dateTmp[0]
    dateMonth=dateTmp[1]
    dateDay = dateTmp[2]  
    doyDay = date[1]
    MJD = date[2]          
    if(doyResult[1].find(',')!=-1):
        gpsWeek = doyResult[1][0:-2]
    else:
        gpsWeek = doyResult[1]
    decimalYear = doyResult[2]

    return render_to_response("doy.html",dict(locals(),**{'username':username,'error':error}))
    
    
def framework(request):
    checkUser(request)  
    return render_to_response("framework.html",{'username':username,'error':error})
    
def changeFrames(request):
    orgFrame = request.GET['orgFrame']
    desFrame = request.GET['desFrame']
    print orgFrame,desFrame
    changeFrame.changeFrame(orgFrame,desFrame)
    return HttpResponse("change succeed")
def dataDownloads(request):
    checkUser(request)
    return render_to_response("dataDownload.html",{'username':username,'error':error})
    
def dataDownloadProcess(request):
    downloadType = request.GET['downloadType']
    station = request.GET['station']
    year_1      =   str(request.GET['startYear'])
    mon_1       =   str(request.GET['startMonth'])
    day_1       =   str(request.GET['startDay'])
    year_2      =   str(request.GET['endYear'])
    mon_2       =   str(request.GET['endMonth'])
    day_2       =   str(request.GET['endDay'])
    print downloadType,station,year_1,mon_1,day_1,year_2,mon_2,day_2
    timelist = dataDownload.intervel(year_1,mon_1,day_1,year_2,mon_2,day_2)
    rmdir=''
    
    if downloadType=='1':
        print 'download 0 file'
        #rmdir = os.path.join(cwd,'data_download/o_files') 
        #print 'rmdir',rmdir
        #os.popen(' cd %s ; rm ./* ' % rmdir)       
        print station
        dataDownload.downloadOfile(timelist,station)
        dataDownload.zipData('o')
    elif downloadType=='2':
        print 'download N file'
        #rmdir = os.path.join(cwd,'data_download/n_files')
        #os.popen(' cd %s ; rm ./* ' % rmdir)
        dataDownload.downloadNfile(timelist)
        dataDownload.zipData('n')
    else:
        print 'download sp3 file'
        #rmdir = os.path.join(cwd,'data_download/sp3_files')
        #print rmdir
        #os.popen(' cd %s ; rm ./* ' % rmdir)
        dataDownload.downloadSp3file(timelist)
        dataDownload.zipData('s')
    
    return HttpResponse('successfully')    
# Create your views here.
