#! /usr/bin/env python
#coding=utf-8

import os,re,linecache,glob
from config import CONFIG

#获取当前路径
#cwd=os.path.dirname(__file__)
cwd=CONFIG.SOFTWAREPATH

    
def track(track_year,track_month,track_day,start_hour,end_hour,sites,now):
    
    #将输入的时刻转换成ABC编码的时刻
    hour=['y','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x']
    #删除上次执行track操作所生成的文件夹及文件，然后建立新的track——process文件夹
    os.popen("cd track ; rm -f -r track_process track_picture log")
    os.popen("cd track ; mkdir track_process track_picture log")
    #将解算和画图所需文件复制进入track_process文件夹里
    os.popen("cp -rf "+os.path.join(cwd,"track/track.cmd")+" "+os.path.join(cwd,"track/track_process"))
    os.popen("cp -rf "+os.path.join(cwd,"track/sh_track ") +os.path.join(cwd,'track/track_process'))
    #根据输入的年月日，转换成所需的GPS天和周，
    parameter=[]
    os.popen("doy %d %d %d | head -1 | awk '{print $6}'>t1" % (track_year,track_month,track_day))
    f=open(os.path.join(cwd,"t1"),'r')
    h=f.read()
    for l in range(start_hour,end_hour+1):
        if int(h)>=100:
            dataname1=str(int(h)) + hour[l]
        if int(h)<100 and int(h)>=10:
            dataname1="0"+str(int(h)) + hour[l]
        if int(h)<10:
            dataname1="00"+str(int(h)) + hour[l]
        #print 'dataname1',dataname1
        parameter.append(dataname1)
    f.close()
    os.popen("doy %d %d %d | tail -n -2 | head -1 | awk '{print $3 $7}' > t2" % (track_year,track_month,track_day))
    f=open(os.path.join(cwd,"t2"),'r')
    t=f.read()
    li=t.split(',') #li[0]存放的是gps week
    
    os.popen("rm t1")
    os.popen("rm t2")

    year = str(track_year)[2:]
    print year
            
    #将与输入的时间对应的数据复制到工作目录========================================
    #datalist=os.listdir(os.path.join(cwd,"track/track_data"))
    datapath = os.path.join(cwd,"track/track_data")
    data_check=[]
    count=0
    
    for h in sites:
        #rem=count
        
        for k in range(0,int(end_hour)-int(start_hour)+1): 
            #print 'k',k 
            #print 'parameter[k]',parameter[k]          
            t=h+parameter[k]+"."+year+"o"
            #print 't',t
            #print os.path.join(datapath,t)
            if os.path.isfile(os.path.join(datapath,t)) == True :
            #for l in datalist:
             #   print 'l',l
	        #for l in datalist:               
             #   if l == t:
                os.popen("cp -rf "+os.path.join(cwd,'track/track_data/%s' % t)+" "+os.path.join(cwd,"track/track_process"))
                #count=count+1
            else:
                
                print type(parameter[k][3])
                data_check.append([h,parameter[k][0:2],parameter[k][3]])
            '''
            if (count != rem+end_hour-start_hour or count==rem): 
                data_check.append([h,parameter[k][0:3]])
            else:
                data_check.append('%dhours' % count)
            '''
    #check_result=[]
    if len(data_check)!=0:
        st = "缺少文件"+'\n'
        for l in data_check:
            print l
            #st = "站点%s缺少第%s天%s小时的数据 " % (str(l[0]),l[1],l[2])+'\n'
            st += "%s%s%s.%so" % (str(l[0]),l[1],l[2],year)+'\n'
            #st += "请仔细检查是否已将相应时间段的文件放入指定文件夹内"
           
        print st
        return st
	        #check_result.append(st)
	#return 'fdsf'
    t="igs"+li[0]+".sp3"
    if os.path.isfile(os.path.join(cwd,"track/track_data/%s" % t)) == False:
        st = "缺少%s文件 获取sp3文件发生错误" % t
        print st
        return st
        
    os.popen("cp -rf "+os.path.join(cwd,"track/sh_mid ") +os.path.join(cwd,'track/track_process'))
    os.popen("cp -rf "+os.path.join(cwd,"track/track_data/%s " % t) +os.path.join(cwd,'track/track_process'))
    #将所有站点开始时刻直到结束时刻对应的数据文件中的数据提取出来，追加到开始时刻对应的文件后面
    
    for l in sites:
        for h in range(1,end_hour-start_hour+1):
            
            t=l+parameter[h]+'.'+year+'o'
            count=len(open(os.path.join(cwd,"track/track_process/%s" % t), 'rU').readlines())
            os.popen("cd track/track_process ; awk 'NR==29,NR==%d' %s>hh" % (count,t))
            w1=open(os.path.join(cwd,"track/track_process/hh"),"r")
            w2=w1.read()
            t1=l+parameter[0]+'.'+year+'o'
            w3=open(os.path.join(cwd,"track/track_process/%s" % t1),'a')
            w3.write(w2)
            w1.close()
            w3.flush()
            w3.close()
            os.popen("cd track/track_process ; rm hh")
    
    
    
    #根据输入的时间修改track.cmd文件内容
    sitesname=[]
    for l in sites:
        if l==sites[0]:
            t="   "+l+" "+l+parameter[0]+"."+year+"o"+" F"
            sitesname.append(t)
            
        else:
            t="   "+l+" "+l+parameter[0]+"."+year+"o"+" k"
            sitesname.append(t)
            
        
    for l in sitesname:
        if l != sitesname[0]:
            t1=open(os.path.join(cwd,"track/track_process/track.cmd"),"r")
            t2=t1.readlines()
            t1.close()
            t2.insert(24,l+"\n")
            t1=open(os.path.join(cwd,"track/track_process/track.cmd"),"w")
            t1.writelines(t2)
            t1.flush()
            t1.close()
    t1=open(os.path.join(cwd,"track/track_process/track.cmd"),"r")
    t2=t1.readlines()
    t1.close()
    t2.insert(24,sitesname[0]+"\n")
    t1=open(os.path.join(cwd,"track/track_process/track.cmd"),"w")
    t1.writelines(t2)
    t1.flush()
    t1.close()
    data1=open(os.path.join(cwd,"track/track_process/track.cmd"))
    t1=data1.read()
    data2=re.sub("nav_file mit12501.sp3 sp3","nav_file igs%s.sp3 sp3" % li[0],t1 )
    data3=open(os.path.join(cwd,"track/track_process/track.cmd"),"wb")
    data3.write(data2)
    data1.close()
    data3.close()
    
    data1=open(os.path.join(cwd,"track/track_process/track.cmd"))
    t1=data1.read()
    data2=re.sub("pos_root TRAK<day>","pos_root %s%s" % (sites[0].upper(),parameter[0]),t1)
    data3=open(os.path.join(cwd,"track/track_process/track.cmd"),"wb")
    data3.write(data2)
    data1.close()
    data3.close()
    
    data1=open(os.path.join(cwd,"track/track_process/track.cmd"))
    t1=data1.read()
    data2=re.sub("res_root TRAK<day>","res_root %s%s" % (sites[0].upper(),parameter[0]),t1)
    data3=open(os.path.join(cwd,"track/track_process/track.cmd"),"wb")
    data3.write(data2)
    data1.close()
    data3.close()
    
    data1=open(os.path.join(cwd,"track/track_process/track.cmd"))
    t1=data1.read()
    data2=re.sub("sum_file TRAK<day>.sum","sum_file %s%s.sum" % (sites[0].upper(),parameter[0]),t1)
    data3=open(os.path.join(cwd,"track/track_process/track.cmd"),"wb")
    data3.write(data2)
    data1.close()
    data3.close() 
    
    
    os.popen("cd track/track_process ; track -f track.cmd -d %s -w %s >! %s_%s.out" % (parameter[0],li[0],sites[0].upper(),parameter[0]))
    #根据输入的时间和相应的站点，将相应的画图命令集成到sh_track里，(sh_track的功能是将数据中最大值最小值提取出来以便于画图)
    os.popen("cp -rf "+os.path.join(cwd,"track/sh_track")+" "+os.path.join(cwd,"track/track_process"))
    referencesites=["f1","f2","f3","f4","f5","f6","f7"]
    outsites=["t.1","t.2","t.3","t4","t.5","t.6","t.7"]
    mid1=["rem1_1","rem1_2","rem1_3","rem1_4"]
    mid2=["rem2_1","rem2_2","rem2_3","rem2_4"]
    i=0
    for l in sites:
        if l!=sites[0]:
            os.popen("cd track/track_process ; set %s = %s%s.NEU.%s.LC" % (referencesites[i],sites[0].upper(),parameter[0],l))
            i=i+1
    i=0
    j=-100

    shmid=open(os.path.join(cwd,"track/track_process/sh_mid"),"a")
    shmid.write("\n")
    i=0
    for l in sites:
        if l!=sites[0]:
            t = "set %s = %s%s.NEU.%s.LC\n" % (referencesites[i],sites[0].upper(),parameter[0],l)
            shmid.write(t)
            i=i+1
    t="set ps = %s%s_eq.pdf\n" % (sites[0].upper(),parameter[0])
    shmid.write(t)
    shmid.write("echo 'Creating $ps'\n")
    i=0
    j=-100
    f=1
    for l in sites:
        if l!=sites[0]:
            t="set %sr = `head -3 $%s | tail -1 | awk '{print $7}'`\ntail -n +3 $%s | awk -v %sr=$%sr '{print ($7-%sr)*1000+(%d)}'  >! %s\nset %sr = `head -3 $%s | tail -1 | awk '{print $9}'`\ntail -n +3 $%s | awk -v %sr=$%sr '{print ($9-%sr)*1000+(%d)}'  >! %s\n" % (referencesites[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],j,mid1[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],j,mid2[f])
            shmid.write(t)
            i=i+1
            f=f+1
            j=j+150   
    shmid.flush()
    shmid.close()
    os.popen("cd track/track_process ; chmod +x sh_mid ; csh -f sh_mid")
    a=[]
    b=[]

    t=glob.glob(os.path.join(cwd,"track/track_process/rem1_*"))
    for l in t:
        count=-1
        for count,line in enumerate(open(l,"rU")):
            pass
        count += 1
        for h in range(1,count):
            context=linecache.getline(l,h)
            a.append(float(context))
        
    min1=min(a)
    max1=max(a)
    t=glob.glob(os.path.join(cwd,"track/track_process/rem2_*"))
    for l in t:
        count=-1
        for count,line in enumerate(open(l,"rU")):
            pass
        count += 1        
        for h in range(1,count):  
            context=linecache.getline(l,h)
            b.append(float(context))
        
    min2=min(b)#提取数据里的最小值用来画图
    max2=max(b)#提取数据里的最大值用来画图   
    shwrite=open(os.path.join(cwd,"track/track_process/sh_track"),"a")
    shwrite.write("\n")
    i=0
    for l in sites:
        if l!=sites[0]:
            t = "set %s = %s%s.NEU.%s.LC\n" % (referencesites[i],sites[0].upper(),parameter[0],l)
            shwrite.write(t)
            i=i+1

        

    
    
    t="set ps = %s%s_all.pdf\necho 'Creating $ps'\n" % (sites[0].upper(),parameter[0])
    shwrite.write(t)

    

    i=0
    j=-100
    for l in sites:
        if l!=sites[0]:
            t="set %sr = `head -3 $%s | tail -1 | awk '{print $7}'`\ntail -n +3 $%s | awk -v %sr=$%sr '{print $18,($7-%sr)*1000+(%d),$8*1000}'  >! %s\n" % (referencesites[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],j,outsites[i])
            shwrite.write(t)


            i=i+1
            j=j+150
    x=(end_hour-start_hour+1)*3600 
    y= (end_hour-start_hour+1)*800                 
    t="psxy %s -R0/%d/%s/%s -JX5/3 -Ba%df200/a100f50:'North (mm)':/SWen -X10 -Y15 -K -W1/255/0/0 -P >! $ps\nawk '{if (NR-int(NR/30)*30 == 0 ) {print $0}}' %s | psxy  -R -JX -Sp -G128/0/0 -K -O >> $ps\n" % (outsites[0],x,min1,max1,y,outsites[0])
    shwrite.write(t)

    i=1
    for l in range(2,len(sites)):
        t="psxy %s -R -JX -K -O -W1/0/0/0 >> $ps\nawk '{if (NR-int(NR/30)*30 == 0 ) {print $0}}' %s | psxy  -R -JX -Sp -G0/0/255 -K -O >> $ps\n" % (outsites[i],outsites[i])
        shwrite.write(t)
        i=i+1     

    t="pstext -R -JX -K -O <<! >> $ps\n"
    shwrite.write(t)
    i=-200
    for l in sites:
        if l != sites[0]:
            t="50 %s 10 0 0 ML %s\n" % (str(i),l.upper())
            shwrite.write(t)
            i=i+200
    shwrite.write("!\n")                


    i=0
    j=-100
    for l in sites:
        if l!=sites[0]:
            t="set %sr = `head -3 $%s | tail -1 | awk '{print $9}'`\ntail -n +3 $%s | awk -v %sr=$%sr '{print $18,($9-%sr)*1000+%d,$10*1000}'  >! %s\n" % (referencesites[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],referencesites[i],j,outsites[i])
            shwrite.write(t)

            i=i+1
            j=j+150
                        
    t="psxy %s -R0/%d/%s/%s -JX5/3 -Ba%df200:'Seconds from %d 00 to %d 00  %d %d, %d':/a100f50:'East (mm)':/SWen -X0 -Y-5.5 -K -O -W1/255/0/0 -P >> $ps\nawk '{if (NR-int(NR/30)*30 == 0 ) {print $0}}' %s | psxy  -R -JX -Sp -G128/0/0 -K -O >> $ps\n" % (outsites[0],x,min2,max2,y,start_hour,end_hour,track_month,track_day,track_year,outsites[0])
    shwrite.write(t)
    i=1
    for l in range(2,len(sites)):
        t="psxy %s -R -JX -K -O -W1/0/0/0 >> $ps\nawk '{if (NR-int(NR/30)*30 == 0 ) {print $0}}' %s | psxy  -R -JX -Sp -G0/0/255 -K -O >> $ps\n" % (outsites[i],outsites[i])
        shwrite.write(t)

        i=i+1  
    t="pstext -R -JX -O <<! >> $ps\n"
    shwrite.write(t)
    i=-200
    for l in sites:
        if l != sites[0]:
            t="50 %s 10 0 0 ML %s\n" % (str(i),l.upper())
            shwrite.write(t)
            i=i+200
    shwrite.write("!\n")  

    shwrite.flush()
    shwrite.close()

    #依次调用track.cmd和sh_track完成数据的解算和画图
    
    
    os.popen("cd track/track_process ; chmod +x sh_track ; csh -f sh_track")
    #os.popen("cp -rf "+os.path.join(cwd,"track/track_process/%s%s_all.png " % (sites[0].upper(),parameter[0])) +os.path.join(cwd,'track/track_picture'))
    os.popen("convert -trim "+os.path.join(cwd,"track/track_process/%s%s_all.pdf " % (sites[0].upper(),parameter[0])) +os.path.join(cwd,'track/track_picture/track%s.png'% now))
    for l in sites:
        os.popen("cp -rf "+os.path.join(cwd,"track/track_process/%s%s.NEU.%s.LC " % (sites[0].upper(),parameter[0],l))+os.path.join(cwd,"track/log"))  
    return ''        
if __name__=='__main__':
    sites=[]
    sites=["cgdm","somt"]
    track_year=2010
    track_month=2
    track_day=25
    start_hour=1
    end_hour=3
    track(track_year,track_month,track_day,start_hour,end_hour,sites,'')
    
    
