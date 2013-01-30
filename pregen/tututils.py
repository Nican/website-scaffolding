import re
import sys
import os
import string
import hashlib
debugmode = False
from subprocess import call

##
# Replaces special characters in a string of unformatted text to HTML special
# character codes.
#
# @param theIn Unformatted source code.
# @return HTML code with special characters properly used.
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

##
# A template print statement for executables that return error codes.
#
# @param executable The name of the executable.
# @param code The error code.
def d_print_return_code(executable,code):
  if code != 0:
    d_print(executable + " return code: " + str(code))

##
# Given a filename, returns the entire contents in a string.
#
# @param filename The file name.
# @return The contents of the file as a string.
def get_file_contents(filename):
  fp = open(filename,'r')
  theMarkup = fp.read()
  fp.close()
  return theMarkup

##
# Template print function that only prints when debug mode is on.
#
# @param string The string to print if debugmode is on.
def d_print(string):
  if debugmode:
    print string

##
# Tries to delete a file and prints an error in the console if it fails.
#
# @param filename The name of the file to delete.
def remove_if_possible(filename):
  try:
    os.remove(filename)
  except Exception, err:
    print "couldn't remove " + filename + " due to error " + str(err)

##
# This function repeatedly calls fn() on markup until it either gets NoneType
# or the same output as input.
#
# @param fn The function to call on markup repeatedly.
# @param markup The markup to run fn() on.
# @return The revised markup after calling fn() on it repeatedly, or NoneType.
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

##
# Execute the command enumerated in callList.  Set shellOnWin to true if you're
# using a Windows Command Prompt.
#
# @param callList A list with the shell command name followed by all params.
# @param shellOnWin True if you're using Windows Command Prompt.
# @return The return code of the program.
def n_call(callList,shellOnWin):
  fnull = open(os.devnull, 'w')
  if shellOnWin and os.name == "nt":
    code = call(callList,stdout=fnull,stderr=fnull,shell=True)
  else:
    code = call(callList,stdout=fnull,stderr=fnull)
  fnull.close()
  if len(callList) > 0:
    d_print_return_code(callList[0],code)
  return code

##
# Write a string of stuff to a given file.  Overwrites existing content.
#
# @param contents The stuff to write to the file.
# @param filename The filename.
def output_file(contents,filename):
  if contents != None:
    fp = open(filename,"wt")
    fp.write(contents)
    fp.close()
  else:
    d_print("contents are null for OutputFile")

##
# Given a list of filenames, call remove_if_possible() on all of them.
#
# @param fileList A list containing filenames to remove.
def remove_all_if_possible(fileList):
  for fileName in fileList:
    remove_if_possible(fileName)

##
# Given a LaTeX excerpt+resolution, returns True if it has already been
# generated, False if not.
#
# @param excerpt The raw LaTeX code.
# @param resolution The resolution.
# @param mediaDir The directory storing the image/media files.
# @return True if the file exists, false if the file does not.
def file_exists(excerpt,resolution,mediaDir):
  filename = make_file_name(excerpt+resolution)
  check = slash_at_end(mediaDir)+filename+".png"
  if os.path.exists(check):
    return True
  return False

##
# Given a string, generate a file name that does not change based on content.
#
# @param excerpt The string.
# @return The file name based on the string.
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

##
# Removes the suffix from a filename. (Unit tested)
#
# @param filename The file name.
# @param suffix The suffix to remove.
# @return The file name without the suffix.
def unsuffix(filename,suffix):
  ind = string.rfind(filename,'.'+suffix)
  return filename[:ind]

##
# Returns the preamble of a LaTeX document as a string.  This is in case we
# ever want to have multiple output formats. (Unit tested)
#
# @param color1 Foreground color (string)
# @param color2 Background color (string)
# @return String containing LaTeX preamble.
def generate_preamble(color1,color2):
  preamble  = '\\documentclass[12pt]{article}\n'
  preamble += '\\usepackage{color}\n'
  preamble += '\\usepackage[dvips]{graphicx}\n'
  preamble += '\\pagestyle{empty}\n'
  preamble += '\\pagecolor{'+color1+'}\n'
  preamble += '\\begin{document}\n'
  preamble += '{\\color{'+color2+'}\n'
  return preamble

##
# Returns the ending of a LaTeX document.  This is in case we ever want to
# have multiple output formats. (Unit tested)
#
# @return The end of a LaTeX document.
def generate_ending():
  return '\\end{document}'

##
# Return the number of non-blank entries in a list of strings.
#
# @param theList
# @return The number of non-blank entries in theList.
def num_non_blanks(theList):
  count = 0
  for i in theList:
    if i != '' and i != '.':
      count += 1
  return count

##
# Ensures there's a slash at the end of theString.
#
# @param theString The string to ensure has a slash at the end.
# @return theString with a slash at the end (if it didn't already).
def slash_at_end(theString):
  if theString[-1] == '/':
    return theString
  else:
    return theString + '/'
