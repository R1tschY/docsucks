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

class Component(object):

  def __init__(self, identifer, name):
    self._id = identifer
    self._name = name

  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name

  def getConfig(self):
    raise NotImplementedError()

  def __hash__(self):
    return hash(self._id)
