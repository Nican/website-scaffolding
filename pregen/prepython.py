import re
import os
import shutil
import hashlib
import codecs
from tututils import *
from subprocess import call

def ShowStuff(markup):
  thePattern = '\nPPY_showstuff (.*?)\Z'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None and matchObject.lastindex >= 1:
    prefix = matchObject.group(1).replace('\n','').replace('\r','')
    if shouldPublish == 'true':
      return re.sub(thePattern,"\n"+prefix+".show()",markup,1,re.DOTALL)
    else:
      return re.sub(thePattern,"\n"+prefix+".savefig('temp/tempout.png')",markup,1,re.DOTALL)
  return markup

def Splice(markup):
  thePattern = 'PPY_splice "(.*?)"\n'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject == None:
    thePattern = 'PPY_splice "(.*?)"\r\n'
    matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None and matchObject.lastindex >= 1:
    print "found"
    try:
      fp = open("splice/"+matchObject.group(1),'rt')
      pycontents = fp.read()
      fp.close()
    except:
      print "Splice: could not open " + matchObject.group(1)
      return None
    result = re.sub(thePattern,pycontents,markup,1,re.DOTALL)
    print result
    return result
  return markup

if __name__ == '__main__':
  shouldPublish = GetNamedArg(sys.argv,'publish','true')
  infile = GetNamedArg(sys.argv,'in','kalman1.ppy')
  outfile = GetNamedArg(sys.argv,'out','kalman1/kalman1.py')
  DPrint("Splice")
  output = ConvertPass(Splice,GetFileContents(infile))
  DPrint("Show")
  output = ConvertPass(ShowStuff,output)
  OutputFile(output,outfile)
