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

import json

def deepupdate(original, update):
  for key, value in original.items():
    if key not in update:
      update[key] = value
    elif isinstance(value, dict):
      deepupdate(value, update[key])
  return update

def generateDefaultConfig(configValueDict):
  return {
    k: v.default_value for k, v in configValueDict.items()
  }


