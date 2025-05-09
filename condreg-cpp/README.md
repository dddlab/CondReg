## Dependencies

### Eigen (C++ template library for linear algebra)

The project uses Eigen 3.4.0 for matrix operations. There are three ways to provide Eigen:

1. **System installation** (recommended for development):
   - Ubuntu/Debian: `sudo apt install libeigen3-dev`
   - macOS: `brew install eigen`
   - Windows: Install via vcpkg or download manually

2. **Automatic download** (default):
   - If Eigen is not found on your system, CMake will automatically download it
   - The download happens only once during the first build
   - The library will be placed in the `lib/eigen` directory

3. **Manual placement**:
   - Download Eigen from https://eigen.tuxfamily.org/
   - Extract it to `lib/eigen` so that `lib/eigen/Eigen/Dense` exists
