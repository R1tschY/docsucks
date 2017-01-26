# -*- coding: utf-8 -*-

import json


def string_escape(string):
  return json.dumps(string)[1:-1]


def to_quoted_string(string):
  return json.dumps(string)


def to_pretty_quoted_string(string):
  result = to_quoted_string(string)
  return result[:-2].replace(r'\n', '\\n"\n"') + result[-2:]
