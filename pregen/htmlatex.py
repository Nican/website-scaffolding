import re
import os
import shutil
import codecs
import StringIO
from tututils import *

if os.name == 'nt':
  pythonexec = "C:\python27\python"
elif os.name == 'posix':
  pythonexec = 'python2.7-32'

def MakeLatexFile(excerpt,tempfile,color1,color2):
  OutputFile(GeneratePreamble(color1,color2)
             +excerpt
             +GenerateEnding(),tempfile)

def CallLatex(tempfile,filename,excerpt):
  latexcode = NCall(["latex", "-interaction=batchmode", tempfile],False)
  if latexcode != 0:
    OutputFile(excerpt + '\n\n' + GetFileContents(tempfile+".log"),filename+".log")
  RemoveAllIfPossible([tempfile+'.log',tempfile+'.aux'])
  if latexcode != 0:
    print "Latex error in:"
    print excerpt
  return latexcode

def CallConvert(dvipscode, tempdir,tempfile,color1,resolution):
  if dvipscode == 0:
    return NCall(["convert",
                  "-antialias",
                  "-transparent",color1,
                  "-density",resolution,
                  tempdir+"/"+tempfile+".eps",
                  tempdir+"/"+tempfile+".png"],True)
  else:
    return 1

def CallDVIPS(latexcode,tempdir,tempfile):
  if latexcode == 0:
    shutil.copy(tempfile+".dvi",tempdir+"/"+tempfile+".dvi")
    dvipscode = NCall(["dvips", "-E", tempdir+"/"+tempfile+".dvi"],False)
    if dvipscode == 0:
      shutil.copy(tempfile+".ps",tempdir+"/"+tempfile+".eps")
    RemoveAllIfPossible([tempfile+'.ps',tempfile+".tex",tempfile+'.dvi',tempdir+"/"+tempfile+".dvi"])
    return dvipscode
  else:
    return 1

def MakePNG(excerpt,resolution):
  # This function borrows heavily from tex2im Version 1.8
  # at http://www.nought.de/tex2im.html .
  filename = MakeFileName(excerpt+resolution)
  tempdir = 'temp'
  tempfile = 'out'
  color1='white'
  color2='black'
  MakeLatexFile(excerpt,tempfile+".tex",color1,color2)
  latexcode = CallLatex(tempfile,filename,excerpt)
  dvipscode = CallDVIPS(latexcode,tempdir,tempfile)
  convertcode = CallConvert(dvipscode, tempdir,tempfile,color1,resolution)
  if convertcode == 0:
    shutil.copy(tempdir+"/"+tempfile+".png","../system/files/"+filename+".png")
  else:
    return None
  return filename

def SpliceTag(markup):
  thePattern = '<splice src="(.*?)" />'
  #print markup
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    theCode = GetFileContents('splice/'+matchObject.group(1))
    return re.sub(thePattern,'<code>'+NBSPize(theCode)+'</code>',markup,1,re.DOTALL)
  return markup

def ShowGraph(markup):
  thePattern = '<showgraph src="(.*?)" />'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    pyoutfile = Unsuffix(matchObject.group(1),'ppy')+'.py'
    pngoutfile = Unsuffix(matchObject.group(1),'ppy')+'.png'
    if os.path.exists("../system/files/"+pngoutfile) == False:
      precode = NCall([pythonexec,'prepython.py','-in='+matchObject.group(1),'-out=temp/'+pyoutfile,'-publish=false'],False)
      if precode == 0:
        graphcode = NCall([pythonexec,'temp/'+pyoutfile],False)
      else:
        DPrint("prepython failed for "+matchObject.group(1))
        return None
      if graphcode != 0:
        DPrint("graph call failed for "+pyoutfile)
        return None
      shutil.copy('temp/tempout.png','../system/files/'+pngoutfile)
    if os.path.exists("../system/files/"+pyoutfile) == False:
      precode = NCall([pythonexec,'prepython.py','-in='+matchObject.group(1),'-out=temp/'+pyoutfile,'-publish=true'],False)
      shutil.copy('temp/'+pyoutfile,'../system/files/'+pyoutfile)
    markup = re.sub(thePattern,'<a href="../../system/files/'+pyoutfile+'.txt"><img src="../../system/files/'+pngoutfile+'" /></a>',markup,1,re.DOTALL)
  return markup

def EquationTag(markup):
  thePattern = '<equation(.*?)>(.*?)</equation>'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    res = GetResolution(matchObject.group(1))
    if FileExists(matchObject.group(2),res,"../system/files/") == False:
      fileName = MakePNG(matchObject.group(2),res)
      if fileName == None:
        DPrint("broken")
        return None
      else:
        fileName = fileName+".png"
        DPrint("wrote " + fileName)
    else:
      fileName = MakeFileName(matchObject.group(2)+res)+".png"
    markup = re.sub(thePattern,'<img src="../../system/files/'+fileName+'">',markup,1,re.DOTALL)
  return markup

inFile = GetArg(sys.argv,1,'kalman1.markup')
outFile = GetArg(sys.argv,2,"kalman1/"+Unsuffix(inFile,'markup')+".html")

print "outfile is " + outFile
DPrint("Equation Tag Pass")
stuff = ConvertPass(EquationTag,GetFileContents(inFile))
DPrint("ShowGraph Tag Pass")
stuff = ConvertPass(ShowGraph,stuff)
DPrint("Splice Tag Pass")
stuff = ConvertPass(SpliceTag,stuff)
OutputFile(stuff,outFile)

# resolution="150x150"
# format="png"
# color1="white"
# color2="black"
# trans=0
# noformula=0
# aa=1
# extra_header="$HOME/.tex2im_header"

#\documentclass[12pt]{article}
#\usepackage{color}
#\usepackage[dvips]{graphicx}
#\pagestyle{empty}
# \pagecolor{$color1}
# \begin{document}
# {\color{$color2}
# \begin{eqnarray*}
#derp
#\end{eqnarray*}}
#\end{document}
