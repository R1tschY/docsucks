# -*- coding: utf-8 -*-

import re

REGEX = re.compile(r"\{\{(?:#([a-z]+)\}\}\n?(.*?)\{\{/\1|([a-z]+))\}\}", re.DOTALL)

def _on_match(ctx, match):
    if match.group(1):
        return "".join(
            REGEX.sub(lambda x: _on_match(dd, x), match.group(2))
            for dd in ctx[match.group(1)])

    return ctx[match.group(3)]


class Renderer(object):

  def __init__(self, **kwargs):
    pass

  def render(self, template, data):
    return REGEX.sub(lambda x: _on_match(data, x), template)


def parse(template):
  return template


