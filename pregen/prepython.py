import re
import os
import shutil
import hashlib
import codecs
from tututils import *
from subprocess import call

##
# Given markup, look for a PPY_showstuff command and replace it with the
# correct Python code to display a graph.  Meant to be used with
# convert_pass().
#
# @param markup The python code to look in.
# @return The python code with a single PPY_showstuff call handled.
def show_stuff(markup):
  thePattern = '\nPPY_showstuff (.*?)\Z'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None and matchObject.lastindex >= 1:
    prefix = matchObject.group(1).replace('\n','').replace('\r','')
    if shouldPublish == 'true':
      return re.sub(thePattern,"\n"+prefix+".show()",markup,1,re.DOTALL)
    else:
      return re.sub(thePattern,"\n"+prefix+".savefig('temp/tempout.png')",markup,1,re.DOTALL)
  return markup

##
# Given a "PPY_splice" command in the code, splice in the given file
# instead. Meant to be used with convert_pass.
#
# @param markup A string containing the Python code with gregstensions.
# @return A string with the Python code + one (and only one) splice done.
def splice(markup):
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
      print "splice: could not open " + matchObject.group(1)
      return None
    result = re.sub(thePattern,pycontents,markup,1,re.DOTALL)
    print result
    return result
  return markup

if __name__ == '__main__':
  shouldPublish = get_named_arg(sys.argv,'publish','true')
  infile = get_named_arg(sys.argv,'in','kalman1.ppy')
  outfile = get_named_arg(sys.argv,'out','kalman1/kalman1.py')
  d_print("splice")
  output = convert_pass(splice,get_file_contents(infile))
  d_print("Show")
  output = convert_pass(show_stuff,output)
  output_file(output,outfile)
