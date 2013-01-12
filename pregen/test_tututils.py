import unittest
from tututils import *

class TutUtilTests(unittest.TestCase):
  def setUp(self):
    pass

  #def test_oneEqualsOne(self):
  #  self.assertEqual(1,2)

  def test_NBSPize(self):
    inStuff = 'class Voltmeter:\n    def __init__(self,_truevoltage,_noiselevel):\n        self.truevoltage = _truevoltage\n        self.noiselevel = _noiselevel\n    def GetVoltage(self):\n        return self.truevoltage\n    def GetVoltageWithNoise(self):\n        return random.gauss(self.GetVoltage(),self.noiselevel)'
    outStuff = 'class Voltmeter:\n&nbsp;&nbsp;&nbsp; def __init__(self,_truevoltage,_noiselevel):\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.truevoltage = _truevoltage\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.noiselevel = _noiselevel\n&nbsp;&nbsp;&nbsp; def GetVoltage(self):\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return self.truevoltage\n&nbsp;&nbsp;&nbsp; def GetVoltageWithNoise(self):\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return random.gauss(self.GetVoltage(),self.noiselevel)\n'
    self.assertEqual(NBSPize(inStuff),outStuff)

  def test_GetNamedArg(self):
    answerpairs = [((['htmlatex','-dir=herp','-snub=derp'],'dir','snerp'),'herp'),
                   ((['htmlatex','-dir=herp','-snub=derp'],'snub','snerp'),'derp'),
                   ((['htmlatex','-dir=herp','-snub=derp'],'snert','snerp'),'snerp')]
    for key in answerpairs:
      result = GetNamedArg(*key[0])
      self.assertEqual(result,key[1])

  def test_GetArg(self):
    answerpairs = [((['htmlatex','herp','derp'],1,'snerp'),'herp'),
                   ((['htmlatex'],1,'snerp'),'snerp'),
                   ((['htmlatex','herp'],1,'snerp'),'herp'),
                   ((['htmlatex','herp','derp'],2,'snerp'),'derp'),
                   ((['htmlatex','herp'],2,'snerp'),'snerp')]
    for key in answerpairs:
      result = GetArg(*key[0])
      self.assertEqual(result,key[1])

  def test_Unsuffix(self):
    self.assertEqual(Unsuffix('derp.markup','markup'),'derp')
    self.assertEqual(Unsuffix('derp.png','png'),'derp')
    self.assertEqual(Unsuffix('derp.anything',''),'derp')
    self.assertEqual(Unsuffix('derp.anything.herp',''),'derp.anything')

  def test_GetResolution(self):
    result = GetResolution('resolution="derp"')
    self.assertEqual(result,'derp')

  def test_GeneratePreamble(self):
    result = GeneratePreamble('herp','derp')
    self.assertEqual(result,'\\documentclass[12pt]{article}\n\\usepackage{color}\n\\usepackage[dvips]{graphicx}\n\\pagestyle{empty}\n\\pagecolor{herp}\n\\begin{document}\n{\\color{derp}\n')

  def test_GenerateEnding(self):
    self.assertEqual(GenerateEnding(),'\\end{document}')

  def test_FindOverallDest(self):
    answerpairs = {('kalman1/','../system/files/'):'../../system/files/',
                   ('kalman1','../system/files/'):'../../system/files/',
                   ('kalman1/derp','../system/files/'):'../../../system/files/',
                   ('kalman1/derp/','../system/files/'):'../../../system/files/',
                   ('kalman1/','../system/files'):'../../system/files/',
                   ('','../system/files'):'../system/files/',
                   ('.','../system/files'):'../system/files/'}
    for key in answerpairs.keys():
      result = FindOverallDest(*key)
      self.assertEqual(result,answerpairs[key])

if __name__ == '__main__':
  unittest.main()
