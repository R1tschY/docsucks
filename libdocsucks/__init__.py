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

version = "0.0"
__version__ = version

from libdocsucks.coreutils import Component

# Data model

class CodeLine(object):

  def __init__(self, line_str=None, expection=None, line_number=None):
    self.line_str = line_str
    self.expection = expection
    self.line_number = line_number


class ModuleTestCode(object):

  def __init__(self, module_name="", test_lines=None):
    self.module_name = module_name
    self.test_lines = [] if not test_lines else test_lines


class Comment(object):

  def __init__(self, comment, commentType=None, lineNumber=None):
    self.comment = comment
    self.type = commentType
    self.lineNumber = lineNumber


class ConfigValue(object):

  def __init__(self, description, default_value):
    self.description = description
    self.default_value = default_value


# Interface

class Language(Component):

  def isSourceFile(self, filename):
    """
    Return true, if file is a source file of this language.
    """
    raise NotImplementedError()

  def getCommentExtractor(self):
    """
    :rtype: CommentExtractor
    """
    raise NotImplementedError()


class DocStyle(Component):

  def extractCodeLines(self, string):
    """
    Extract all code lines from the doc string (``string``).
    
    >>> docstyle.extractCodeLines('''
    ...  The anwser
    ...  >>> 41 + 1
    ...  42
    ... ''')
    ModuleTestCode("", [CodeLine("41 + 1", "42")])
    
    :type string: str
    :rtype: ModuleTestCode
    """
    raise NotImplementedError()


class CommentExtractor(object):

  def extractComments(self, file):
    """
    Return Iterable, with extracted Comments from ``file``.
    :rtype: iterable of ``Comment``
    """
    raise NotImplementedError()


class TestCodeGenerator(Component):

  def generateTest(self, moduleTestCode, filename, config):
    """
    Generate test suite for test code lines. 
    
    :param moduleTestCode: test code lines
    :type moduleTestCode: ModuleTestCode
    
    :param filename: file name for file to create
    :type filename: str
    """
    raise NotImplementedError()


# Registry

class ComponentRegistry(object):

  def __init__(self):
    self.languages = {}
    self.docstyles = {}
    self.generators = {}
    self.defaultDocStyles = {}
    self.defaultGenerators = {}

  def registerLanguage(self, language):
    self.languages[language.id] = language

  def registerDocstyle(self, docstyle):
    self.docstyles[docstyle.id] = docstyle

  def registerGenerator(self, generator):
    self.generators[generator.id] = generator

  def setDefaultDocStyle(self, languageid, docstyleid):
    self.defaultDocStyles[languageid] = docstyleid

  def getDefaultDocStyle(self, languageid):
    docstyleid = self.defaultDocStyles.get(languageid, None)
    return self.docstyles.get(docstyleid, None) if docstyleid else None

  def setDefaultGenerator(self, languageid, generatorid):
    self.defaultGenerators[languageid] = generatorid

  def getDefaultGenerator(self, languageid):
    generatorid = self.defaultGenerators.get(languageid, None)
    return self.generators.get(generatorid, None) if generatorid else None


registry = ComponentRegistry()

def RegisteredLanguage():
  def RegisteredLanguageId(cls):
    registry.registerLanguage(cls())
    return cls
  return RegisteredLanguageId

def RegisteredDocstyle(defaultFor=None):
  if not defaultFor:
    defaultFor = ()

  if isinstance(defaultFor, str):
    defaultFor = (defaultFor,)

  def RegisteredDocstyleId(cls):
    docstyle = cls()
    registry.registerDocstyle(docstyle)
    for default in defaultFor:
      registry.setDefaultGenerator(default, docstyle.id)
    return cls
  return RegisteredDocstyleId

def RegisteredGenerator(defaultFor=None):
  if not defaultFor:
    defaultFor = ()

  if isinstance(defaultFor, str):
    defaultFor = (defaultFor,)

  def RegisteredGeneratorId(cls):
    generator = cls()
    registry.registerGenerator(generator)
    for default in defaultFor:
      registry.setDefaultGenerator(default, generator.id)
    return cls
  return RegisteredGeneratorId
