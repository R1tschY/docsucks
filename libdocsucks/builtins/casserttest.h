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

#include <cstdio>

namespace docsucks {

class test_case
{
  test_case(const test_case&); // = delete
  test_case& operator=(const test_case&); // = delete
public:
  test_case();
  ~test_case();

  const char* get_stdout() const { return membuf_stdout_; }
  void reset() {
    fflush(stdout);
    fseek(stdout, 0, SEEK_END);
    long size = ftell(stdout);
    frewind(stdout);

    memset(membuf_stdout_, 0, size);
  }

private:
  FILE* old_stdout_ = nullptr;

  FILE* mem_stdout_ = nullptr;
  char* membuf_stdout_ = nullptr;
  std::size_t memlen_stdout_ = 0;
};

inline
void test_case::test_case()
{
  fflush(stdout);

  mem_stdout_ = open_memstream(&membuf_stdout_, &memlen_stdout_);
  if (!mem_stdout_)
  {
    fprintf(stderr, "Failed to create memstream for stdout: errno=%d", errno);
    throw std::exception("Failed to create memstream for stdout");
  }

  // replace stdout
  old_stdout_ = stdout;
  stdout = mem_stdout_;
}

inline
void test_case::~test_case()
{
  fflush(stdout);

  // restore stdout
  stdout = old_stdout_;

  if (mem_stdout_)
  {
    fclose(mem_stdout_);
    free(membuf_stdout_);
  }
}

} // namespace docsucks
