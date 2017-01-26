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

import os
import json
import libdocsucks

from libdocsucks.config import generateDefaultConfig
from libdocsucks.builtins import load_builtins

DEFAULT_GENERATED_FOLDER = "."

class DocSucks(object):

  def __init__(self, language=None):
    self.registry = libdocsucks.registry
    self.language = language
    self.config = {}

    load_builtins()

  def showRegisteredComponents(self):
    print("registered languages: {}".format(", ".join(self.registry.languages.keys())))
    print("registered docstyles: {}".format(", ".join(self.registry.docstyles.keys())))
    print("registered generators: {}".format(", ".join(self.registry.generators.keys())))
    print("")
    print("default docstyles: {}".format(self.registry.defaultDocStyles))
    print("default generators: {}".format(self.registry.defaultGenerators))

  def handleFile(self, filename, output_path=None):
    if not os.path.exists(filename):
      raise IOError("file `{}` does not exist".format(filename))

    language = self.getLanguage(filename)
    extractor = self.getExtractor(language)
    docstyle = self.getDocStyle(language)
    generator = self.getGenerator(language)

    if not extractor:
      raise Exception("no extractor for language {}".format(language.id))

    if not docstyle:
      raise Exception("no docstyle for language {}".format(language.id))

    if not generator:
      raise Exception("no generator for language {}".format(language.id))

    if output_path is None:
      output_path = self.getGeneratedFilenameFor(filename)

    with open(filename, "r") as infile:
      comments = (docstyle.extractCodeLines(comment)
                  for comment in extractor.extractComments(infile))
      generator.generateTest(
        comments, output_path, filename,
        self.getGeneratorConfig(generator))

  def findLanguageForFile(self, filename):
    for language in self.registry.languages.values():
      if language.isSourceFile(filename):
        return language

  def getLanguage(self, filename):
    if self.language is None:
      language = self.findLanguageForFile(filename)
      if not language:
        raise Exception("no language for filename `{}`".format(filename))
      return language
    else:
      return self.language

  def getLanguageConfig(self, language):
    return self._getComponentConfig("language", language)

  def getExtractor(self, language):
    return language.getCommentExtractor()

  def getExtractorConfig(self, extractor):
    return self._getComponentConfig("extractor", extractor)

  def getDocStyle(self, language):
    return self.registry.getDefaultDocStyle(language.id)

  def getDocStyleConfig(self, docstyle):
    return self._getComponentConfig("docstyle", docstyle)

  def getGenerator(self, language):
    return self.registry.getDefaultGenerator(language.id)

  def getGeneratorConfig(self, generator):
    return self._getComponentConfig("generator", generator)

  def getGeneratedFilenameFor(self, filename):
    base, ext = os.path.splitext(os.path.basename(filename))
    return os.path.join(DEFAULT_GENERATED_FOLDER,
                        "{base}DocTest.{ext}".format(base=base, ext=ext))

  def handleFiles(self, filenames):
    for filename in filenames:
      self.handleFile(filename)

  def loadConfig(self, filename):
    with open(filename, "r") as f:
      self.config.update(json.load(f))

  def _getComponentConfig(self, component_type, component):
    config = generateDefaultConfig(component.getConfig())
    config.update(self.config.get(component_type, {}))
    config.update(self.config.get(component.id, {}))
    return config

