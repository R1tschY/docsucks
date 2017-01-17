# -*- coding: utf-8 -*-
#
# libdocsucks -- generate tests for code in documentation
#
# Copyright 2017 Richard Liebscher.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import subprocess
import os
import sys
import shlex

from os import path
from testtools import TestCase
from libdocsucks.utils import tuplify
from io import StringIO

def path_escape(string):
  return string.replace('<>?":|\/*', "_")


class CppCodeTest(TestCase):

  def setUp(self):
    super(CppCodeTest, self).setUp()
    self.compileMatrix = {}
    self.buildDir = "."
    self.outfiletemplate = "{compiler}/{flags}/{basename}Test"
    self.testargs = ()

  def _compile(self, filename, compiler, flags, outfile):
    args = tuplify(compiler, filename, *shlex.split(flags), "-o", outfile)

    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = "\n".join(o.decode("utf-8") for o in [proc.stdout, proc.stderr])
    if output:
      print(" ".join(args))
      print(output)
    self.assertEqual(0, proc.returncode, "compile of `{}` failed".format(filename))

  def _run(self, exe):
    retval = subprocess.call(
      tuplify(exe, *self.testargs),
      stdout=sys.stdout, stderr=sys.stderr)
    self.assertEqual(0, retval, "{} failed".format(
      os.path.splitext(os.path.basename(exe))[0]))

  def assertRunsFineForFlags(self, filename, compiler, flags):
    outfile = path.join(self.buildDir, self.outfiletemplate.format(
      compiler=path_escape(compiler),
      flags=path_escape(flags),
      basename=path.splitext(os.path.basename(filename))[0]
    ))

    folder = path.dirname(path.normpath(outfile))
    if not path.isdir(folder):
      os.makedirs(folder)

    if (not path.exists(outfile)
        or path.getmtime(filename) > path.getmtime(outfile)):
      self._compile(filename, compiler, flags, outfile)

    self._run(outfile)

  def assertRunsFineFor(self, filename, compiler):
    flags = self.compileMatrix.get(compiler, None)

    if not flags:
      return self.assertRunsFineForFlags(filename, compiler, "")

    if isinstance(flags, str):
      return self.assertRunsFineForFlags(filename, compiler, flags)

    for flag in flags:
      self.assertRunsFineForFlags(filename, compiler, flag)

  def assertRunsFine(self, filename):
    for compiler in self.compileMatrix.keys():
      self.assertRunsFineFor(filename, compiler)





