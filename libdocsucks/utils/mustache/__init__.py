# -*- coding: utf-8 -*-

import logging

# choose mustache implementation
try:
  # pystache
  from pystache import parse, Renderer

  logging.info('As mustache implementation `pystache` is choosen.')

except ImportError:
  # fallback
  from libdocsucks.utils.mustache.fallback import parse, Renderer

  logging.warning('As mustache implementation fallback is choosen. '
                  'Install `pystache` for better performance and less bugs.')