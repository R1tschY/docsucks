///
/// Copyright (c) 2017 R1tschY
/// 
/// Permission is hereby granted, free of charge, to any person obtaining a copy
/// of this software and associated documentation files (the "Software"), to 
/// deal in the Software without restriction, including without limitation the 
/// rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
/// sell copies of the Software, and to permit persons to whom the Software is
/// furnished to do so, subject to the following conditions:
/// 
/// The above copyright notice and this permission notice shall be included in
/// all copies or substantial portions of the Software.
/// 
/// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
/// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
/// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
/// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
/// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
/// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
/// IN THE SOFTWARE.
///


#pragma once

#include <string>


namespace docsucks {

std::string to_repr(signed char x) { return "static_cast<signed char>(" + std::to_string(x) + ")"; }
std::string to_repr(short x) { return "static_cast<short>(" + std::to_string(x) + ")"; }
std::string to_repr(int x) { return std::to_string(x); }
std::string to_repr(long x) { return std::to_string(x) + "L"; }
std::string to_repr(long long x) { return std::to_string(x) + "LL"; }

std::string to_repr(unsigned char x) { return "static_cast<unsigned char>(" + std::to_string(x) + ")"; }
std::string to_repr(unsigned short x) { return "static_cast<unsigned short>(" + std::to_string(x) + ")"; }
std::string to_repr(unsigned int x) { return std::to_string(x) + "U"; }
std::string to_repr(unsigned long x) { return std::to_string(x) + "UL"; }
std::string to_repr(unsigned long long x) { return std::to_string(x) + "ULL"; }

std::string to_repr(float x) { return std::to_string(x) + "f"; }
std::string to_repr(double x) { return std::to_string(x); }
std::string to_repr(long double x) { return std::to_string(x) + "L"; }

std::string to_repr(const char* x) { return "\"" + std::string(x) + "\""; }
std::string to_repr(const std::string& x) { return "std::string(" + std::string(x) + ")"; }
std::string to_repr(const std::wstring& x) { return "std::wstring(L" + std::string(x) + ")"; }


} // namespace docsucks


