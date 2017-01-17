#define BOOST_TEST_MODULE casserttest
#define BOOST_TEST_DYN_LINK

#include "../../builtins/casserttest.h"
#include <boost/test/unit_test.hpp>

#include <iostream>
#include <cstdio>

using namespace docsucks;

BOOST_AUTO_TEST_SUITE(CAssert_TestCase)

BOOST_AUTO_TEST_CASE(stdio_printf)
{
  std::string out;
  {
    test_case tc;
    printf("42");
    out = tc.get_stdout();
  }
  BOOST_CHECK_EQUAL("42", out);

  {
    test_case tc;
    printf("0x%x", 0x42);
    out = tc.get_stdout();
  }
  BOOST_CHECK_EQUAL("0x42", out);

}

BOOST_AUTO_TEST_CASE(stdio_puts)
{
  std::string out;
  {
    test_case tc;
    puts("42");
    out = tc.get_stdout();
  }
  BOOST_CHECK_EQUAL("42\n", out);

  {
    test_case tc;
    fputs("555", stdout);
    out = tc.get_stdout();
  }
  BOOST_CHECK_EQUAL("555", out);

  {
    test_case tc;
    puts("");
    fputs("555", stdout);
    puts("x10");
    out = tc.get_stdout();
  }
  BOOST_CHECK_EQUAL("\n555x10\n", out);
}

BOOST_AUTO_TEST_CASE(stdio_iostream)
{
  std::string out;
  {
    test_case tc;
    std::cout << 42 << std::endl;
    out = tc.get_stdout();
  }
  BOOST_CHECK_EQUAL("42\n", out);

  {
    test_case tc;
    std::cout << 555 << "_kmh" << std::endl;
    std::cout << 678 << std::endl;
    out = tc.get_stdout();
  }
  BOOST_CHECK_EQUAL("555_kmh\n678\n", out);
}

BOOST_AUTO_TEST_CASE(stdio_get_stdout)
{
  std::string out;
  {
    test_case tc;
    std::cout << 42 << std::endl;
    out = tc.get_stdout();
    std::cout << 24 << std::endl;
    out = tc.get_stdout();
  }
  BOOST_CHECK_EQUAL("42\n24\n", out);

  {
    test_case tc;
    std::cout << 42 << std::endl;
    out = tc.get_stdout();
    std::cout << 245 << std::endl;
    out = tc.get_stdout();
  }
  BOOST_CHECK(strcmp("42\n24\n", out.c_str()) != 0);
}

BOOST_AUTO_TEST_CASE(stdio_reset)
{
  std::string out1;
  std::string out2;
  std::string out3;

  {
    test_case tc;
    std::cout << 42 << std::endl;
    out1 = tc.get_stdout();
    tc.reset();

    std::cout << 24 << std::endl;
    out2 = tc.get_stdout();
    tc.reset();

    std::cout << 555 << std::endl;
    out3 = tc.get_stdout();
  }

  BOOST_CHECK_EQUAL("42\n", out1);
  BOOST_CHECK_EQUAL("24\n", out2);
  BOOST_CHECK_EQUAL("555\n", out3);
}
BOOST_AUTO_TEST_SUITE_END()
