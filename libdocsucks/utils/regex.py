# -*- coding: utf-8 -*-

import re


def lined_re_find(regex, string, group=0):
  pos = 0
  lineno = 1
  for match in regex.finditer(string):
    end = match.start(group)
    lineno += string.count("\n", pos, end)
    pos = end

    yield (lineno, match)
