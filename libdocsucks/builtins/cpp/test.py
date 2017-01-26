# -*- coding: utf-8 -*-

import libdocsucks.utils.mustache as mustache
from libdocsucks import TestCodeGenerator, ConfigValue
from libdocsucks.builtins.cpp.utils import to_pretty_quoted_string
from os import path
import libdocsucks

def generateInclude(include, relativeInclude=True):
  if relativeInclude:
    return '#include {}'.format(to_pretty_quoted_string(include))
  else:
    return '#include <{}>'.format(include)

def generateUsing(using):
  return 'using namespace {};'.format(using)


class CppTestGenerator(TestCodeGenerator):

  def __init__(self, identifer, name):
    super(CppTestGenerator, self).__init__(identifer, name)

    self.required_includes = ()
    self.renderer = mustache.Renderer(missing_tags='ignore', escape=lambda u: u)

  def generateTest(self, moduleTestCodeList, filename, source_filename, config):
    if not path.isabs(source_filename):
      source_filename = "./" + source_filename

    includes = [source_filename]
    includes.extend(self.required_includes)
    includes.extend(config.get("includes", ()))

    data = {
      "docsucks": "docsucks " + libdocsucks.version,
      "includes": "\n".join(generateInclude(include) for include in includes),
      "usings": "\n".join(generateUsing(using) for using in config.get("namespaces", ())),
    }

    data["testCases"] = [
        {
          "testCase": [
            {
              "code": x.line_str,
              "stdout_exp": to_pretty_quoted_string(x.expection if x.expection else "")
            }
            for x in moduleTestCode.test_lines
          ]
        }
        for moduleTestCode in moduleTestCodeList
        if moduleTestCode
    ]

    fileCode = self.renderer.render(self.template, data)
    print(fileCode)

    with open(filename, "w") as f:
      f.write(fileCode)


  def getConfig(self):
    return {
      "namespaces": ConfigValue(
        description="List of namespaces to include a `using namespace ...`",
        default_value=("std",)
      ),
      "includes": ConfigValue(
        description="List of includes to add. "
          "Includes starting with a dot are included through double quotes.",
        default_value=()
      ),
    }


