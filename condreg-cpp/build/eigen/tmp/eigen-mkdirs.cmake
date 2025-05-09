# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen/src/eigen"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen/src/eigen-build"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen/tmp"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen/src/eigen-stamp"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen/src"
  "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen/src/eigen-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen/src/eigen-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/Users/lordine/stat_research/CondReg/condreg-cpp/build/eigen/src/eigen-stamp${cfgdir}") # cfgdir has leading slash
endif()
