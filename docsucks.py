#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# docsucks -- generate tests for code in documentation
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

'''
@author:     R1tschY
@copyright:  2017 R1tschY. All rights reserved.
@license:    Apache License, Version 2.0
'''

import sys
import json

import libdocsucks
from libdocsucks.generate import DocSucks

from argparse import ArgumentParser, RawDescriptionHelpFormatter

PROGRAM_NAME = "docsucks"

def main(args):
  program_version_message = '{} v{}'.format(PROGRAM_NAME, libdocsucks.version)
  program_license = '''%s

Copyright 2017 Richard Liebscher

Licensed under the Apache License, Version 2.0 (the "License").
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

  try:
    # Setup argument parser
    parser = ArgumentParser(
      description=program_license,
      formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
      "-v", "--verbose",
      dest="verbose",
      action="count",
      help="print extra information for debugging")

    parser.add_argument(
      '-V', '--version',
      action='version',
      version=program_version_message)

    parser.add_argument(
      '-c', '--config',
      metavar="path",
      default=None,
      help="use this config file")

    parser.add_argument(
      dest="paths",
      help="paths source file(s)",
      metavar="path",
      nargs='+')

    # Process arguments
    args = parser.parse_args()

    docsucks = DocSucks()

    if args.config:
      docsucks.loadConfig(args.config)

    if args.verbose:
      print("== components")
      docsucks.showRegisteredComponents()

      print("\n== config")
      print(json.dumps(docsucks.config, indent=2))
      print("")

    docsucks.handleFiles(args.paths)
    return 0

  except KeyboardInterrupt:
    # handle keyboard interrupt
    return 0

  except Exception as e:
    indent = len(PROGRAM_NAME) * " "
    sys.stderr.write(PROGRAM_NAME + ": " + repr(e) + "\n")
    sys.stderr.write(indent + "  for help use --help")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))


