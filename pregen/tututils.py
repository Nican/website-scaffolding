import re
import sys
import os
import string
import hashlib
debugmode = True
from subprocess import call

def nbspize(theIn):
  thePattern = '([ ]+?) (\S)'
  lines = theIn.split('\n')
  res = ''
  for l in lines:
    done = False
    l = l.replace('>','&gt;')
    l = l.replace('<','&lt;')
    while not done:
      matchObject = re.search(thePattern,l,re.DOTALL)
      if matchObject != None:
        repped = matchObject.group(1).replace(' ','&nbsp;')
        newString = repped + ' ' + matchObject.group(2)
        l = re.sub(thePattern,newString,l,1,re.DOTALL)
      else:
        done = True
    if l != '':
      res += l + '\n'
  return res

def d_print_return_code(executable,code):
  if code != 0:
    d_print(executable + " return code: " + str(code))

def get_file_contents(filename):
  fp = open(filename,'r')
  theMarkup = fp.read()
  fp.close()
  return theMarkup

def d_print(string):
  if debugmode:
    print string

def remove_if_possible(filename):
  try:
    os.remove(filename)
  except Exception, err:
    print "couldn't remove " + filename + " due to error " + str(err)

def convert_pass(fn,markup):
  if markup != None:
    done = False
    while not done:
      res = fn(markup)
      if res == None:
        return None
      if markup == res:
        done = True
      markup = res
    return markup
  return None

def n_call(callList,shellOnWin):
  fnull = open(os.devnull, 'w')
  if shellOnWin and os.name == "nt":
    code = call(callList,stdout=fnull,stderr=fnull,shell=True)
  else:
    code = call(callList,stdout=fnull)
  fnull.close()
  if len(callList) > 0:
    d_print_return_code(callList[0],code)
  return code

def output_file(contents,filename):
  if contents != None:
    fp = open(filename,"wt")
    fp.write(contents)
    fp.close()
  else:
    d_print("contents are null for OutputFile")

def remove_all_if_possible(fileList):
  for fileName in fileList:
    remove_if_possible(fileName)

def file_exists(excerpt,resolution,mediaDir):
  filename = make_file_name(excerpt+resolution)
  check = slash_at_end(mediaDir)+filename+".png"
  if os.path.exists(check):
    return True
  return False

def make_file_name(excerpt):
  theHash = hashlib.sha256()
  theHash.update(excerpt)
  return theHash.hexdigest()

# Unit tested
def get_named_arg(argv,argname,defaultArg):
  argPattern = '-(.*?)=(.*)'
  for i in argv:
    matchObj = re.search(argPattern,i,re.DOTALL)
    if matchObj != None and matchObj.group(1) == argname:
      return matchObj.group(2)
  return defaultArg

# Unit tested
def get_arg(argv,num,defaultArg):
  if len(argv) >= num+1:
    return argv[num]
  return defaultArg

# Unit tested
def get_resolution(argstring):
  resPattern = 'resolution="(.*?)"'
  matchObj = re.search(resPattern,argstring,re.DOTALL)
  if matchObj != None:
    return matchObj.group(1)
  return '250x250'

# Unit tested
def unsuffix(filename,suffix):
  ind = string.rfind(filename,'.'+suffix)
  return filename[:ind]

# Unit tested
def generate_preamble(color1,color2):
  preamble  = '\\documentclass[12pt]{article}\n'
  preamble += '\\usepackage{color}\n'
  preamble += '\\usepackage[dvips]{graphicx}\n'
  preamble += '\\pagestyle{empty}\n'
  preamble += '\\pagecolor{'+color1+'}\n'
  preamble += '\\begin{document}\n'
  preamble += '{\\color{'+color2+'}\n'
  return preamble

# Unit tested
def generate_ending():
  return '\\end{document}'

def num_non_blanks(theList):
  count = 0
  for i in theList:
    if i != '' and i != '.':
      count += 1
  return count

def slash_at_end(theString):
  if theString[-1] == '/':
    return theString
  else:
    return theString + '/'
