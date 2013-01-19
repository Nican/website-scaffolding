import re
import os
import shutil
from tututils import *

if os.name == 'nt':
  pythonexec = "C:\python27\python"
elif os.name == 'posix':
  if os.uname()[0] == 'Darwin':
    pythonexec = 'python2.7-32'
  else:
    pythonexec = 'python'

def make_latex_file(excerpt,tmpfile,color1,color2):
  output_file(generate_preamble(color1,color2)+excerpt+generate_ending(),tmpfile)

##
# First step of LaTeX PNG conversion.  Runs latex to get a DVI file.
#
# @param tmpfile The name of the DVI file to generate.
# @param filename The auto-generated filename to use (usually a hash).
# @param excerpt The raw LaTeX code to parse.
# @return The return code of the latex command.
def call_latex(tmpfile,filename,excerpt):
  latexcode = n_call(["latex", "-interaction=batchmode", tmpfile],False)
  if latexcode != 0:
    output_file(excerpt + '\n\n' + get_file_contents(tmpfile+".log"),
               filename+".log")
  remove_all_if_possible([tmpfile+'.log',tmpfile+'.aux'])
  if latexcode != 0:
    print "Latex error in:"
    print excerpt
  return latexcode

##
# Final step of LaTeX PNG conversion.  Converts the EPS file to a PNG.
#
# @param dvipscode The return code of the dvips command.  Should be 0 to work.
# @param tmpdir The temp directory to put the intermediate files.
# @param tmpfile The name of the ps and eps files to generate.
# @param color1 The transparency color to pass to convert.
# @param resolution The resolution to render the EPS at.
# @return The return code of the convert command or 1 if latexcode is not 0.
def call_convert(dvipscode, tmpdir,tmpfile,color1,resolution):
  if dvipscode == 0:
    return n_call(["convert",
                  "-antialias",
                  "-transparent",color1,
                  "-density",resolution,
                  tmpdir+tmpfile+".eps",
                  tmpdir+tmpfile+".png"],True)
  else:
    return 1

##
# Intermediate step of LaTeX PNG conversion.  Converts the DVI file to an EPS
# file so it can be converted to PNG in the next step.
#
# @param latexcode The return code of the latex command.  Should be 0 to work.
# @param tmpdir The temp directory to put the intermediate files.
# @param tmpfile The name of the ps and eps files to generate.
# @return The return code of the dvips command or 1 if latexcode is not 0.
def call_dvips(latexcode,tmpdir,tmpfile):
  if latexcode == 0:
    shutil.copy(tmpfile+".dvi",tmpdir+tmpfile+".dvi")
    dvipscode = n_call(["dvips", "-E", tmpdir+tmpfile+".dvi"],False)
    if dvipscode == 0:
      shutil.copy(tmpfile+".ps",tmpdir+tmpfile+".eps")
    remove_all_if_possible([tmpfile+'.ps',
                            tmpfile+".tex",
                            tmpfile+'.dvi',
                            tmpdir+tmpfile+".dvi"])
    return dvipscode
  else:
    return 1

##
# Creates a PNG file out of the LaTeX excerpt that comes in, and with the
# resolution specified in resolution.  If blank, it uses the default resolution
# in get_resolution().
#
# @param excerpt The LaTeX code to turn to PNG.
# @param resolution A string defining the resolution to use.
# @return The filename to a new PNG file containing the typeset equation.
def make_png(excerpt,resolution):
  # This function borrows heavily from tex2im Version 1.8
  # at http://www.nought.de/tex2im.html .
  filename = make_file_name(excerpt+resolution)
  tempfile = 'out'
  color1='white'
  color2='black'
  make_latex_file(excerpt,tempfile+".tex",color1,color2)
  latexcode = call_latex(tempfile,filename,excerpt)
  dvipscode = call_dvips(latexcode,tempdir,tempfile)
  convertcode = call_convert(dvipscode, tempdir,tempfile,color1,resolution)
  if convertcode == 0:
    shutil.copy(tempdir+tempfile+".png",relPath+filename+".png")
  else:
    return None
  return filename

##
# Checks the markup for a splice tag, and replaces the tag with a code snippet
# div using a style meant for code snippets. Does it once and then stops.
# Repeat using convert_pass to do it to the whole document.
#
# @param markup The markup to check for a splice tag.
# @return The revised markup.
def splice_tag(markup):
  thePattern = '<splice src="(.*?)" />'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    theCode = get_file_contents('splice/'+matchObject.group(1))
    return re.sub(thePattern,
                  '<div class="snippet">'+nbspize(theCode)+'</div>',
                  markup,1,re.DOTALL)
  return markup

##
# Checks the markup for a showgraph tag, runs prepython on it, runs the script,
# and replaces the showgraph tag with an img tag with the correct png.  Does
# it once and then stops.  Repeat using convert_pass to do it to the whole
# document.
#
# @param markup The markup to check for a showgraph tag.
# @return The revised markup.
def show_graph(markup):
  thePattern = '<showgraph src="(.*?)" />'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    pyoutfile = unsuffix(matchObject.group(1),'ppy')+'.py'
    pngoutfile = unsuffix(matchObject.group(1),'ppy')+'.png'
    if not os.path.exists(relPath+pngoutfile):
      precode = n_call([pythonexec,
                       '../prepython.py',
                       '-in='+matchObject.group(1),
                       '-out=temp/'+pyoutfile,
                       '-publish=false'],False)
      if precode == 0:
        graphcode = n_call([pythonexec,'temp/'+pyoutfile],False)
      else:
        d_print("prepython failed for "+matchObject.group(1))
        return None
      if graphcode != 0:
        d_print("graph call failed for "+pyoutfile)
        return None
      shutil.copy('temp/tempout.png',relPath+pngoutfile)
    if not os.path.exists(relPath+pyoutfile):
      precode = n_call([pythonexec,
                       '../prepython.py',
                       '-in='+matchObject.group(1),
                       '-out=temp/'+pyoutfile,
                       '-publish=true'],False)
      shutil.copy('temp/'+pyoutfile,relPath+pyoutfile)
    markup = re.sub(thePattern,'<a href="'+webPath+pyoutfile+
                    '.txt"><img src="'+webPath+pngoutfile+'" />'+
                    '</a>',markup,1,re.DOTALL)
  return markup

##
# Checks the markup for an equation tag, runs LaTeX on it, and replaces it
# with an img tag with the correct png.  Does it once and then stops.  Repeat
# using convert_pass to do it to the whole document.
#
# @param markup The markup to check for a markup tag.
# @return The revised markup.
def equation_tag(markup):
  thePattern = '<equation(.*?)>(.*?)</equation>'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    res = get_resolution(matchObject.group(1))
    if not file_exists(matchObject.group(2),res,relPath):
      fileName = make_png(matchObject.group(2),res)
      if fileName == None:
        d_print("broken")
        return None
      else:
        fileName = fileName+".png"
        d_print("wrote " + fileName)
    else:
      fileName = make_file_name(matchObject.group(2)+res)+".png"
    markup = re.sub(thePattern,
                    '<img src="'+webPath+fileName+'">',
                    markup,1,re.DOTALL)
  return markup

if __name__ == '__main__':
  inFile = get_arg(sys.argv,1,'kalman1.markup')
  outFile = get_arg(sys.argv,2,"kalman1/"+unsuffix(inFile,'markup')+".html")
  relPath = get_arg(sys.argv,3,'../system/files/')
  webPath = get_arg(sys.argv,4,'../../system/files/')
  tempdir = get_arg(sys.argv,5,'temp/')

  d_print("Equation Tag Pass")
  stuff = convert_pass(equation_tag,get_file_contents(inFile))
  d_print("ShowGraph Tag Pass")
  stuff = convert_pass(show_graph,stuff)
  d_print("Splice Tag Pass")
  stuff = convert_pass(splice_tag,stuff)
  output_file(stuff,outFile)
