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

"""
C++ support for docsucks
"""

from libdocsucks import Language, registry
from libdocsucks.builtins.comments import CRegexExtractor

# TODO: option: in string comments?

class CppLanguage(Language):

  def __init__(self):
    super(CppLanguage, self).__init__("c++", "C++")

    self.sourceFileExts = (".h", ".hpp", ".hxx", ".cpp", ".cc", ".cxx")
    self.extractor = CRegexExtractor()

  def isSourceFile(self, filename):
    return any(
      filename.endswith(ext)
      for ext in self.sourceFileExts
    )

  def getCommentExtractor(self):
    return self.extractor

registry.registerLanguage(CppLanguage())





