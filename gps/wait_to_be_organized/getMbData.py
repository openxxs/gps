import os

#cwd=os.path.dirname(__file__)
cwd=os.getcwd()

def getMbData(station):
    
    orgdir = os.path.join(cwd,'experiment/vsoln')
    desdir = os.path.join(cwd,'exp2nd/TimeSeries_accuracy')
    print cwd
    for s in station:
        s=s.upper()
        for n in range(1,4):
            desmb = 'mb_%s.dat%d' % (s,n)
            desdir = os.path.join(cwd,'exp2nd/TimeSeries_accuracy')
            orgmb = 'mb_%s.dat%d' % (s,n)
            cmd = 'cd %s ; mv %s %s ; cp -f %s %s' % (orgdir,orgmb,desmb,desmb,desdir)
            print cmd
            os.popen('cd %s ; mv %s %s ; cp -f %s %s' % (orgdir,orgmb,desmb,desmb,desdir))       
        #os.popen('cd %s ; cp -f ./mb_%s.dat* %s' % (os.path.join(cwd,'experiment/vsoln'),s,os.path.join(cwd,'exp2nd/TimeSeries_accuracy')))                
        os.popen('cd %s ; ./mbDataCollect.sh %s' % (desdir,s))  
if __name__ == '__main__':
    getMbData(['7001', 'WLSN', 'JPLM'])
