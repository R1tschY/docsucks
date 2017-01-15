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

import unittest
from libdocsucks.builtins.comments import CRegexExtractor

class CRegexExtractorTest(unittest.TestCase):

  def testMultipleLineComments(self):
    cre = CRegexExtractor(in_strings=False)

    self._assertExtractedComment(
      cre,
      """
      /* my file */        
      """,
      (" my file ",)
    )

    self._assertExtractedComment(
      cre,
      """    
      /*
      multiline
      */ 
      /**
       * line 1
       * line 2
       */  
      """,
      ("""
      multiline
      """, """*
       * line 1
       * line 2
       """)
    )

    # comment in expression
    self._assertExtractedComment(
      cre,
      """
      int i1 = 3 */* comment */ 6;
      int i2 = 3 /* comment */* 6;
      """,
      (" comment ", " comment ")
    )

    # comment in string
    self._assertExtractedComment(
      cre,
      """
      const char* evalstr = "++/* no comment */++";
      const char* evalstr2 = "++/* no comment ++";
      """,
      ()
    )

  def testSingleLineComments(self):
    cre = CRegexExtractor(in_strings=False)

    self._assertExtractedComment(
      cre,
      """
      // one line comment
      /// one line doc
      //> one line qtdoc
      """,
      (" one line comment", "/ one line doc", "> one line qtdoc")
    )

    self._assertExtractedComment(
      cre,
      '''
      const char* evalstr3 = "++// no comment */++";
      const char* evalstr4 = "++++" /* comment */; // line comment
      const char* evalstr5 = "++++ // line
      /* no */      
      ";
      ''',
      (" comment ", " line comment")
    )

#    self._assertExtractedComment(
#      cre,
#      '''
#      const char* evalstr6 = "\" /* eval */ "; // good \"
#      ''',
#      (" comment ", " line comment", ' good \\"')
#    )

    # comment in comment
    self._assertExtractedComment(
      cre,
      """
      // eval /*
      struct C { };
      // eval */ end
      """,
      (" eval /*", " eval */ end")
    )

  def _assertExtractedComment(self, cre, code, comments):
    from io import StringIO

    with StringIO(code) as f:
      self.assertEqual(
        tuple(comment for comment in cre.extractComments(f)),
        comments
      )


if __name__ == '__main__':
    unittest.main()
