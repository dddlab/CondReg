cmake_minimum_required(VERSION 3.10)
project(condreg VERSION 0.1.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add include paths
include_directories(include)

# Find Eigen
find_package(Eigen3 QUIET NO_MODULE)
if(NOT Eigen3_FOUND)
  # If Eigen wasn't found through the package system, look in lib/eigen
  if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/lib/eigen/Eigen/Dense)
    include_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib/eigen)
    message(STATUS "Using bundled Eigen in lib/eigen")
  else()
    message(STATUS "Eigen not found via find_package or in lib/eigen.")
    message(STATUS "Downloading Eigen...")
    
    # Create the lib/eigen directory
    file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib/eigen)
    
    # Updated to use a different approach for downloading Eigen
    include(FetchContent)
    FetchContent_Declare(
      eigen
      URL https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
      # Remove the hash check as it's causing issues
    )
    FetchContent_MakeAvailable(eigen)
    
    # Set include path
    include_directories(${eigen_SOURCE_DIR})
    
    # Set flag to indicate we need to add dependency and custom command later
    set(NEED_EIGEN_DEPENDENCY TRUE)
    set(NEED_EIGEN_COPY TRUE)
  endif()
endif()

# Add the library
add_library(condreg STATIC
    src/path_solvers.cpp
    src/utils.cpp
    src/condreg.cpp
)

# Now that the library target exists, we can add the dependency if needed
if(DEFINED NEED_EIGEN_DEPENDENCY)
    add_dependencies(condreg eigen)
endif()

# Add custom command to copy Eigen if needed
if(DEFINED NEED_EIGEN_COPY)
    add_custom_command(
      TARGET condreg POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${eigen_SOURCE_DIR}/Eigen
        ${CMAKE_CURRENT_SOURCE_DIR}/lib/eigen/Eigen
      COMMENT "Copying Eigen to lib/eigen directory"
    )
endif()

# Link with Eigen if found through find_package
if(Eigen3_FOUND)
  target_link_libraries(condreg Eigen3::Eigen)
endif()

# Enable testing
enable_testing()

# Add test executables
add_executable(test_path_solvers test/test_path_solvers.cpp)
target_link_libraries(test_path_solvers condreg)
add_test(NAME test_path_solvers COMMAND test_path_solvers)

add_executable(test_utils test/test_utils.cpp)
target_link_libraries(test_utils condreg)
add_test(NAME test_utils COMMAND test_utils)

add_executable(test_condreg test/test_condreg.cpp)
target_link_libraries(test_condreg condreg)
add_test(NAME test_condreg COMMAND test_condreg)

# Setup examples directory if it exists
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/examples/CMakeLists.txt)
    add_subdirectory(examples)
else()
    message(STATUS "No examples/CMakeLists.txt found, skipping examples")
endif()

# Install targets
install(TARGETS condreg
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# Install headers
install(DIRECTORY include/ DESTINATION include)

# Generate API documentation with Doxygen
find_package(Doxygen)
if(DOXYGEN_FOUND)
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/doc/Doxyfile.in)
        set(DOXYGEN_IN ${CMAKE_CURRENT_SOURCE_DIR}/doc/Doxyfile.in)
        set(DOXYGEN_OUT ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)

        configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
        
        add_custom_target(doc
            COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Generating API documentation with Doxygen"
            VERBATIM
        )
    else()
        message(STATUS "doc/Doxyfile.in not found, skipping documentation generation")
    endif()
endif()