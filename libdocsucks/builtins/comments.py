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
from libdocsucks import CommentExtractor, Comment


def dropNones(iterable):
  return (x for x in iterable if x is not None)


class CRegexExtractor(CommentExtractor):

  def __init__(self, in_strings=True):
    regex = r'/(?:(/.*?)$|(\*.*?)\*/)'
    if not in_strings:
      regex = r'"[^"]*"|' + regex  # TODO: cannot handle escaped quote

    self.regex = re.compile(regex, re.DOTALL | re.MULTILINE)

  def _processMatch(self, match):
    match = match.group(1) or match.group(2)
    if not match: return None

    return Comment(
      match[1:],
      commentType='//' if match[0] == '/' else '/*')

  def extractComments(self, file):
    return dropNones(
      self._processMatch(m)
      for m in self.regex.finditer(file.read())
    )


