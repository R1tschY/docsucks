//
// libdocsucks -- generate tests for code in documentation
//
// Copyright 2017 Richard Liebscher.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

// activate always the assertions
#ifdef NDEBUG
#undef NDEBUG
#endif

// assertion lib
#include <cassert>

#include <unistd.h>
#include <cstdio>
#include <cstring>
#include <cerrno>
#include <stdexcept>


namespace docsucks {

class test_case
{
  test_case(const test_case&); // = delete
  test_case& operator=(const test_case&); // = delete
public:
  test_case();
  ~test_case();

  std::string get_stdout() const
  {
    fflush(stdout);
    long pos = ftell(stdout);

    std::string result(pos, '\0');
    fseek(stdout, 0, SEEK_SET);
    std::fread(&result[0], sizeof(result[0]), result.size(), stdout);
    fseek(stdout, pos, SEEK_SET);
    return result;
  }

  void reset()
  {
    fflush(stdout);
    rewind(stdout);
  }

private:
  int old_stdout_ = 0;
};

inline
test_case::test_case()
{
  old_stdout_ = dup(fileno(stdout));

  FILE* file = freopen("tmp.stdout~", "w+", stdout);
  if (file == NULL)
  {
    perror("freopen() failed");
    throw std::runtime_error("Failed to create tempfile for stdout");
  }
}

inline
test_case::~test_case()
{
  fflush(stdout);

  dup2(old_stdout_, fileno(stdout));
  close(old_stdout_);
}

} // namespace docsucks
