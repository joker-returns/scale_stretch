import matlab.engine
import os
import StringIO

out = StringIO.StringIO()
err = StringIO.StringIO()

print "[+] Attempting to start Matlab Engine"
engine = matlab.engine.start_matlab()
print "[+] Done starting engine"
cdir = os.getcwd()
print "[+] Current Working Directory is {}".format(cdir)
chdir = engine.chdir(cdir + "/matlab")
print "[+] Current Working Directory is {}".format(cdir)
def doDemo(r1,r2):
    engine.Demo(r1,r2,nargout=0,stdout=out)


