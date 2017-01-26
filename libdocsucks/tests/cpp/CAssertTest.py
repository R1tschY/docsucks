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

from os import path

from libdocsucks.tests import CppCodeTest
from libdocsucks.generate import DocSucks

TEST_FILE_DIR = path.normpath(
  path.join(path.dirname(__file__), "..", "..", "..", "testfiles"))

class CAssertTest(CppCodeTest):

  def setUp(self):
    super(CAssertTest, self).setUp()
    self.buildDir = path.join(path.dirname(__file__), "..", "..", "..", "build", "tests", "cpp")
    self.compileMatrix = {
      "g++": [
#        "-std=gnu++03 -lboost_unit_test_framework",
        "-std=gnu++0x -lboost_unit_test_framework",
        "-std=gnu++1y -lboost_unit_test_framework",
        "-std=gnu++1z -lboost_unit_test_framework"
      ]
    }

  def testUnits(self):
    self.assertRunsFine(path.join(path.dirname(__file__), "CAssertTest.cpp"))

  def testIntegration(self):
    docsucks = DocSucks()
    docsucks.loadConfig(path.join(TEST_FILE_DIR, "CppClass.json"))
    docsucks.handleFile(
      path.join(TEST_FILE_DIR, "CppClass.h"),
      output_path=path.join(self.buildDir, "CppClassDocTest.cpp"))
    self.assertRunsFine(path.join(self.buildDir, "CppClassDocTest.cpp"))


