import os

#cwd=os.path.dirname(__file__)
cwd = os.getcwd()

def getMax_MinFromFile(orgFile,counts):
    #desFile = '/home/bxy/GPS/trunk/data_results/file_tmp'
    desFile = os.path.join(cwd,'data_results/file_tmp')
    for i in counts:
        cmd = "cat %s | awk 'BEGIN{max=-1999999;min=19999999} {if($%d>max) {max=$%d} if($%d<min) {min=$%d}} END{print max ,min}' >> %s " % (orgFile,i,i,i,i,desFile)
        print cmd
        os.popen(cmd)
    
    tmpFile = open(desFile,'r')
    result = tmpFile.readlines()
    print result
    os.popen('rm %s' % desFile)
    return result

if __name__=='__main__':
    getMax_MinFromFile('/home/bxy/GPS/trunk/data_results/usud/mp1.txt',[1,2])
