#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from __future__ import division
import os,glob
import commands


#cwd=os.path.dirname(__file__)
cwd=os.getcwd()

def getData(typename):                             #extract data into baseline.data
    baseline_path = ''
    if typename == 'baseline':
        baseline_path=os.path.join(cwd,'exp2nd/baseline')
        filepath = os.path.join(baseline_path,'baseline.dat')
        if os.path.isfile(filepath):
            os.remove(filepath)      
    elif typename == 'batch':
        baseline_path=os.path.join(cwd,'exp2nd/baseline_batch')  
        
    oscala_path=os.path.join(cwd,'exp2nd/oscala_%s/oscala.*' % typename)
        
    list_files = os.popen("dir %s" % oscala_path).read().split() 
    list_files.sort()  #按时间顺序排列文件
    print list_files
    
    for l in list_files:
        
        #cmd="awk '{BEGIN{ORS=""}}{if($2~/[0-9]X$/){i=1; while(i<NF-2){print $i%s; i++}}{print %s}}' %s >> %sbaseline.txt" % (space,line,l,baseline_path)
        #cmd = "awk '{if($2~/[0-9]X$/ && $3~/N/) print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18}' %s >> %sbaseline.txt" %(l,baseline_path)
        cmd = "awk '{if($2~/[0-9]X$/ && $3~/N/) print $0}' %s >> %s/baseline.dat" %(l,baseline_path)
        os.popen(cmd)

if __name__ == '__main__':
    getData('batch')
    #getData('baseline')
