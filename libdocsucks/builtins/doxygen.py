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

import re
from libdocsucks import DocStyle, ModuleTestCode, CodeLine, registry

def isDocComment(comment):
  string = comment.comment
  if comment.type == "/*":
    return string.startswith("*") or string.startswith("!")
  else:  # comment.type == "//"
    return (
      (string.startswith("/") and not string.startswith("//"))
      or string.startswith("!")
    )

class DoxygenStyle(DocStyle):

  def __init__(self):
    super(DoxygenStyle, self).__init__("doxygen", "Doxygen")

    self.regex = re.compile(
      r"[\\@]code(?:{[^}]*})?(.*?)[\\@]endcode",
      re.DOTALL)



  def _preprocessComment(self, comment):
    lines = comment.comment.splitlines()

    if comment.type == "/*":
      lines = self._preprocessMultilineComment(lines)
    elif comment.type == "//":
      lines = self._preprocessSingleComment(lines)

    return "\n".join(lines)

  def _preprocessMultilineComment(self, lines):
    newlines = []
    newlines.append(lines[0].lstrip("*!"))
    newlines.extend(
      line.lstrip().lstrip("*")
      for line in lines[1:]
    )
    return newlines

  def _preprocessSingleComment(self, lines):
    return (line[1:] for line in lines)

  def extractCodeLines(self, comment):
    if not isDocComment(comment):
      return ()

    doc = self._preprocessComment(comment)
    testCodeList = []
    for match in self.regex.finditer(doc):
      testCodeList.append(CodeLine(match.group(1)))

    return ModuleTestCode("", testCodeList)


registry.registerDocstyle(DoxygenStyle())
registry.setDefaultDocStyle("c", "doxygen")
registry.setDefaultDocStyle("c++", "doxygen")




