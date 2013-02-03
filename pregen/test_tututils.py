import unittest
from tututils import *

class TutUtilTests(unittest.TestCase):
  def setUp(self):
    pass

  ##
  # Tests the nbspize() function.
  def test_nbspize(self):
    inStuff = 'class Voltmeter:\n    def __init__(self,_truevoltage,_noiselevel):\n        self.truevoltage = _truevoltage\n        self.noiselevel = _noiselevel\n    def GetVoltage(self):\n        return self.truevoltage\n    def GetVoltageWithNoise(self):\n        return random.gauss(self.GetVoltage(),self.noiselevel)'
    outStuff = 'class Voltmeter:\n&nbsp;&nbsp;&nbsp; def __init__(self,_truevoltage,_noiselevel):\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.truevoltage = _truevoltage\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; self.noiselevel = _noiselevel\n&nbsp;&nbsp;&nbsp; def GetVoltage(self):\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return self.truevoltage\n&nbsp;&nbsp;&nbsp; def GetVoltageWithNoise(self):\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return random.gauss(self.GetVoltage(),self.noiselevel)\n'
    self.assertEqual(nbspize(inStuff),outStuff)

  ##
  # Tests the get_named_arg() function.
  def test_get_named_arg(self):
    answerpairs = [((['htmlatex','-dir=herp','-snub=derp'],'dir','snerp'),'herp'),
                   ((['htmlatex','-dir=herp','-snub=derp'],'snub','snerp'),'derp'),
                   ((['htmlatex','-dir=herp','-snub=derp'],'snert','snerp'),'snerp')]
    for key in answerpairs:
      result = get_named_arg(*key[0])
      self.assertEqual(result,key[1])

  ##
  # Tests the get_arg() function.
  def test_get_arg(self):
    answerpairs = [((['htmlatex','herp','derp'],1,'snerp'),'herp'),
                   ((['htmlatex'],1,'snerp'),'snerp'),
                   ((['htmlatex','herp'],1,'snerp'),'herp'),
                   ((['htmlatex','herp','derp'],2,'snerp'),'derp'),
                   ((['htmlatex','herp'],2,'snerp'),'snerp')]
    for key in answerpairs:
      result = get_arg(*key[0])
      self.assertEqual(result,key[1])

  ##
  # Tests the unsuffix() function.
  def test_unsuffix(self):
    self.assertEqual(unsuffix('derp.markup','markup'),'derp')
    self.assertEqual(unsuffix('derp.png','png'),'derp')
    self.assertEqual(unsuffix('derp.anything',''),'derp')
    self.assertEqual(unsuffix('derp.anything.herp',''),'derp.anything')

  ##
  # Tests the get_resolution() function.
  def test_get_resolution(self):
    result = get_resolution('resolution="derp"')
    self.assertEqual(result,'derp')

  ##
  # Tests the generate_preamble() function.
  def test_generate_preamble(self):
    result = generate_preamble('herp','derp')
    self.assertEqual(result,'\\documentclass[12pt]{article}\n\\usepackage{color}\n\\usepackage[dvips]{graphicx}\n\\pagestyle{empty}\n\\pagecolor{herp}\n\\begin{document}\n{\\color{derp}\n')

  ##
  # Tests the generage_ending() function.
  def test_generate_ending(self):
    self.assertEqual(generate_ending(),'\\end{document}')

if __name__ == '__main__':
  unittest.main()
