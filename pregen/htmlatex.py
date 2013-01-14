import re
import os
import shutil
#import codecs
#import StringIO
from tututils import *

if os.name == 'nt':
  pythonexec = "C:\python27\python"
elif os.name == 'posix':
  print os.uname()
  if os.uname()[0] == 'Darwin':
    print "mac mode"
    pythonexec = 'python2.7-32'
  else:
    pythonexec = 'python'

def MakeLatexFile(excerpt,tmpfile,color1,color2):
  OutputFile(GeneratePreamble(color1,color2)+excerpt+GenerateEnding(),tmpfile)

def CallLatex(tmpfile,filename,excerpt):
  latexcode = NCall(["latex", "-interaction=batchmode", tmpfile],False)
  if latexcode != 0:
    OutputFile(excerpt + '\n\n' + GetFileContents(tmpfile+".log"),
               filename+".log")
  RemoveAllIfPossible([tmpfile+'.log',tmpfile+'.aux'])
  if latexcode != 0:
    print "Latex error in:"
    print excerpt
  return latexcode

def CallConvert(dvipscode, tmpdir,tmpfile,color1,resolution):
  if dvipscode == 0:
    return NCall(["convert",
                  "-antialias",
                  "-transparent",color1,
                  "-density",resolution,
                  tmpdir+tmpfile+".eps",
                  tmpdir+tmpfile+".png"],True)
  else:
    return 1

def CallDVIPS(latexcode,tmpdir,tmpfile):
  if latexcode == 0:
    shutil.copy(tmpfile+".dvi",tmpdir+tmpfile+".dvi")
    dvipscode = NCall(["dvips", "-E", tmpdir+tmpfile+".dvi"],False)
    if dvipscode == 0:
      shutil.copy(tmpfile+".ps",tmpdir+tmpfile+".eps")
    RemoveAllIfPossible([tmpfile+'.ps',
                         tmpfile+".tex",
                         tmpfile+'.dvi',
                         tmpdir+tmpfile+".dvi"])
    return dvipscode
  else:
    return 1

def MakePNG(excerpt,resolution):
  # This function borrows heavily from tex2im Version 1.8
  # at http://www.nought.de/tex2im.html .
  filename = MakeFileName(excerpt+resolution)
  tempfile = 'out'
  color1='white'
  color2='black'
  MakeLatexFile(excerpt,tempfile+".tex",color1,color2)
  latexcode = CallLatex(tempfile,filename,excerpt)
  dvipscode = CallDVIPS(latexcode,tempdir,tempfile)
  convertcode = CallConvert(dvipscode, tempdir,tempfile,color1,resolution)
  if convertcode == 0:
    shutil.copy(tempdir+tempfile+".png",relPath+filename+".png")
  else:
    return None
  return filename

def SpliceTag(markup):
  thePattern = '<splice src="(.*?)" />'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    theCode = GetFileContents('splice/'+matchObject.group(1))
    return re.sub(thePattern,
                  '<div class="snippet">'+NBSPize(theCode)+'</div>',
                  markup,1,re.DOTALL)
  return markup

def ShowGraph(markup):
  thePattern = '<showgraph src="(.*?)" />'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    pyoutfile = Unsuffix(matchObject.group(1),'ppy')+'.py'
    pngoutfile = Unsuffix(matchObject.group(1),'ppy')+'.png'
    if not os.path.exists(relPath+pngoutfile):
      precode = NCall([pythonexec,
                       '../prepython.py',
                       '-in='+matchObject.group(1),
                       '-out=temp/'+pyoutfile,
                       '-publish=false'],False)
      if precode == 0:
        graphcode = NCall([pythonexec,'temp/'+pyoutfile],False)
      else:
        DPrint("prepython failed for "+matchObject.group(1))
        return None
      if graphcode != 0:
        DPrint("graph call failed for "+pyoutfile)
        return None
      shutil.copy('temp/tempout.png',relPath+pngoutfile)
    if not os.path.exists(relPath+pyoutfile):
      precode = NCall([pythonexec,
                       '../prepython.py',
                       '-in='+matchObject.group(1),
                       '-out=temp/'+pyoutfile,
                       '-publish=true'],False)
      shutil.copy('temp/'+pyoutfile,relPath+pyoutfile)
    markup = re.sub(thePattern,'<a href="'+webPath+pyoutfile+
                    '.txt"><img src="'+webPath+pngoutfile+'" />'+
                    '</a>',markup,1,re.DOTALL)
  return markup

def EquationTag(markup):
  thePattern = '<equation(.*?)>(.*?)</equation>'
  matchObject = re.search(thePattern,markup,re.DOTALL)
  if matchObject != None:
    res = GetResolution(matchObject.group(1))
    if not FileExists(matchObject.group(2),res,relPath):
      fileName = MakePNG(matchObject.group(2),res)
      if fileName == None:
        DPrint("broken")
        return None
      else:
        fileName = fileName+".png"
        DPrint("wrote " + fileName)
    else:
      fileName = MakeFileName(matchObject.group(2)+res)+".png"
    markup = re.sub(thePattern,
                    '<img src="'+webPath+fileName+'">',
                    markup,1,re.DOTALL)
  return markup

if __name__ == '__main__':
  inFile = GetArg(sys.argv,1,'kalman1.markup')
  outFile = GetArg(sys.argv,2,"kalman1/"+Unsuffix(inFile,'markup')+".html")
  relPath = GetArg(sys.argv,3,'../system/files/')
  webPath = GetArg(sys.argv,4,'../../system/files/')
  tempdir = GetArg(sys.argv,5,'temp/')

  print "outfile is " + outFile
  DPrint("Equation Tag Pass")
  stuff = ConvertPass(EquationTag,GetFileContents(inFile))
  DPrint("ShowGraph Tag Pass")
  stuff = ConvertPass(ShowGraph,stuff)
  DPrint("Splice Tag Pass")
  stuff = ConvertPass(SpliceTag,stuff)
  OutputFile(stuff,outFile)
