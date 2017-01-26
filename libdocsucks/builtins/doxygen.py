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
import operator
from libdocsucks.utils.regex import lined_re_find
import itertools


CODE, VERBATIM = range(2)

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
    self.vregex = re.compile(
      r"[\\@]verbatim(.*?)[\\@]endverbatim",
      re.DOTALL)

  def _preprocessComment(self, comment):
    """
    preprocess comment and return comment text only containing documentation.
    """
    lines = comment.comment.splitlines()

    if comment.type == "/*":
      lines = self._preprocessMultilineComment(lines)
    elif comment.type == "//":
      lines = self._preprocessSingleComment(lines)

    return "\n".join(lines)

  def _preprocessMultilineComment(self, lines):
    """
    strip * and ! from first line and support multiple line comment starting
    with star. 
    """
    newlines = []
    newlines.append(lines[0].lstrip("*!"))

    for line in lines[1:]:
      stripped = line.lstrip()
      if stripped.startswith("*"):
        newlines.append(stripped.lstrip("*"))
      else:
        newlines.append(line)

    return newlines

  def _preprocessSingleComment(self, lines):
    """
    remove doc string indicator: / and ! 
    """
    return (line[1:] for line in lines)

  def extractCodeLines(self, comment):
    if not isDocComment(comment):
      return ()

    doc = self._preprocessComment(comment)

    # generate list of code and verbatim blocks
    testCodeList = itertools.chain([
      (CODE, lineno, match.group(1))
      for lineno, match in lined_re_find(self.regex, doc, group=1)
    ], [
      (VERBATIM, lineno, match.group(1))
      for lineno, match in lined_re_find(self.vregex, doc, group=1)
    ])

    # order by line number
    testCodeList = sorted(testCodeList, key=operator.itemgetter(1))

    testList = []
    i = 0
    while i < len(testCodeList) - 1:
      if testCodeList[i][0] == 1:
        i += 1
        continue

      if testCodeList[i + 1][0] == VERBATIM:
        testList.append(CodeLine(testCodeList[i][2],
                                 expection=testCodeList[i + 1][2].strip() + '\n',
                                 line_number=testCodeList[i][1]))
        i += 2
      else:
        testList.append(CodeLine(testCodeList[i][2],
                                 line_number=testCodeList[i][1]))
        i += 1

    if i < len(testCodeList) and testCodeList[i][0] == CODE:
      testList.append(CodeLine(testCodeList[i][2],
                               line_number=testCodeList[i][1]))

    return ModuleTestCode("", testList)


registry.registerDocstyle(DoxygenStyle())
registry.setDefaultDocStyle("c", "doxygen")
registry.setDefaultDocStyle("c++", "doxygen")




