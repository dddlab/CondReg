#!/usr/bin/env python3
"""
Cross-platform build script for condreg-cpp library.
This script builds the C++ library required by the Python bindings.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and handle errors"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        raise

def find_cmake():
    """Find cmake executable"""
    cmake_names = ['cmake', 'cmake3']
    for name in cmake_names:
        if shutil.which(name):
            return name
    raise RuntimeError("CMake not found. Please install CMake.")

def build_cpp_library():
    """Build the C++ library"""
    # Get paths
    script_dir = Path(__file__).parent
    cpp_dir = script_dir.parent / "condreg-cpp"
    build_dir = cpp_dir / "build"
    
    if not cpp_dir.exists():
        raise RuntimeError(f"C++ source directory not found: {cpp_dir}")
    
    print(f"Building C++ library in: {cpp_dir}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    # Create build directory
    build_dir.mkdir(exist_ok=True)
    
    # Find cmake
    cmake = find_cmake()
    
    # Configure build
    cmake_args = [cmake, ".."]
    
    # Platform-specific configuration
    if platform.system() == "Windows":
        # Use Visual Studio generator on Windows
        cmake_args.extend([
            "-G", "Visual Studio 16 2019",  # or newer
            "-A", "x64",
            "-DCMAKE_BUILD_TYPE=Release"
        ])
    else:
        # Use Unix Makefiles or Ninja on Unix-like systems
        if shutil.which("ninja"):
            cmake_args.extend(["-G", "Ninja"])
        cmake_args.extend([
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_POSITION_INDEPENDENT_CODE=ON"
        ])
    
    # Add Eigen path if specified
    if "EIGEN_INCLUDE_DIR" in os.environ:
        eigen_path = os.environ["EIGEN_INCLUDE_DIR"]
        cmake_args.append(f"-DEIGEN3_INCLUDE_DIR={eigen_path}")
    
    print("Configuring with CMake...")
    run_command(cmake_args, cwd=build_dir)
    
    # Build
    build_args = [cmake, "--build", ".", "--config", "Release"]
    
    # Add parallel build on Unix
    if platform.system() != "Windows":
        import multiprocessing
        build_args.extend(["--", f"-j{multiprocessing.cpu_count()}"])
    
    print("Building...")
    run_command(build_args, cwd=build_dir)
    
    # Verify library was built
    if platform.system() == "Windows":
        lib_patterns = ["Release/condreg.lib", "Debug/condreg.lib", "condreg.lib"]
    else:
        lib_patterns = ["libcondreg.a", "libcondreg.so"]
    
    lib_found = False
    for pattern in lib_patterns:
        lib_path = build_dir / pattern
        if lib_path.exists():
            print(f"✓ Library built successfully: {lib_path}")
            lib_found = True
            break
    
    if not lib_found:
        print("Warning: Could not find built library file")
        print("Contents of build directory:")
        for item in build_dir.rglob("*"):
            if item.is_file():
                print(f"  {item.relative_to(build_dir)}")
    
    return True

def install_dependencies():
    """Install build dependencies"""
    print("Installing build dependencies...")
    
    # Check for required tools
    required_tools = []
    
    if not shutil.which("cmake"):
        required_tools.append("cmake")
    
    if platform.system() == "Windows":
        # Check for Visual Studio or Build Tools
        vs_paths = [
            "C:/Program Files (x86)/Microsoft Visual Studio/2019",
            "C:/Program Files/Microsoft Visual Studio/2022",
            "C:/BuildTools"
        ]
        vs_found = any(os.path.exists(path) for path in vs_paths)
        if not vs_found:
            print("Warning: Visual Studio or Build Tools for Visual Studio not found")
            print("Please install Visual Studio 2019 or later, or Build Tools for Visual Studio")
    
    if required_tools:
        print(f"Missing required tools: {', '.join(required_tools)}")
        print("Please install them using your system package manager:")
        
        if platform.system() == "Darwin":  # macOS
            print("  brew install cmake")
        elif platform.system() == "Linux":
            print("  sudo apt-get install cmake build-essential  # Ubuntu/Debian")
            print("  sudo yum install cmake gcc-c++             # CentOS/RHEL")
        elif platform.system() == "Windows":
            print("  Install CMake from https://cmake.org/download/")
            print("  Install Visual Studio Build Tools")
        
        return False
    
    return True

def main():
    """Main function"""
    print("=== Cross-platform C++ Library Builder ===")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--check-deps":
        success = install_dependencies()
        sys.exit(0 if success else 1)
    
    try:
        if not install_dependencies():
            print("Please install missing dependencies and try again.")
            sys.exit(1)
        
        build_cpp_library()
        print("✓ Build completed successfully!")
        
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 