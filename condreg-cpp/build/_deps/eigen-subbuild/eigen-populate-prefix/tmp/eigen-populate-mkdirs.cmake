# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-src"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-build"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-subbuild/eigen-populate-prefix"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-subbuild/eigen-populate-prefix/tmp"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-subbuild/eigen-populate-prefix/src/eigen-populate-stamp"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-subbuild/eigen-populate-prefix/src"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-subbuild/eigen-populate-prefix/src/eigen-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-subbuild/eigen-populate-prefix/src/eigen-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/Users/lordine/stat_research/CondReg/condreg-cpp/build/_deps/eigen-subbuild/eigen-populate-prefix/src/eigen-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
