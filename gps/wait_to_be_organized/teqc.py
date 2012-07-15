import linecache,os

#cwd=os.path.dirname(__file__)
cwd=os.getcwd()

def readfile(rfile):
    tmp = os.path.join(cwd,'data_results/data_tmp')
    os.popen(" awk '{if($1~/^SUM/) print $0}' %s > %s " % (rfile,tmp)) 
    context=open(tmp,'r').read()    
    li=context.split()
    context= [li[12], li[14], li[15]]
    print context
    return context

if __name__=='__main__':
    readfile('/home/bxy/GPS/trunk/usud0100.10S')



