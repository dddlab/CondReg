from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import sys
import os
import platform
import pybind11

__version__ = '0.1.0'

# Locate condreg-cpp and Eigen
root_dir = os.path.dirname(os.path.abspath(__file__))
condreg_cpp_dir = os.path.abspath(os.path.join(root_dir, '..', 'condreg-cpp'))
condreg_cpp_include = os.path.join(condreg_cpp_dir, 'include')
EIGEN_INCLUDE_DIR = os.path.abspath(os.path.join('/opt/homebrew/include/eigen3'))

# Detect Python version
python_version = ".".join(map(str, sys.version_info[:2]))
print(f"Building for Python {python_version}")
print(f"Using Eigen headers from: {EIGEN_INCLUDE_DIR}")
print(f"Using condreg-cpp from: {condreg_cpp_dir}")

class get_pybind_include:
    """Helper class to determine the pybind11 include path"""
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        return pybind11.get_include(self.user)

def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler."""
    import tempfile
    import subprocess
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except Exception:
            return False
    return True

def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag."""
    flags = ['-std=c++14', '-std=c++11']
    for flag in flags:
        if has_flag(compiler, flag): return flag
    raise RuntimeError('Unsupported compiler -- at least C++11 support is needed!')

class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.9']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts + ['-Wl,-rpath,{}'.format(os.path.join(condreg_cpp_dir, 'build'))]
        build_ext.build_extensions(self)

# Only build extensions when explicitly requested
if 'build_ext' in sys.argv:
    ext_modules = [
        Extension(
            'condreg_cpp',
            ['src/bindings.cpp'],
            include_dirs=[
                # Add the include directory here
                condreg_cpp_include,
                # Path to pybind11 headers
                get_pybind_include(),
                get_pybind_include(user=True),
                # Path to Eigen headers
                EIGEN_INCLUDE_DIR
            ],
            libraries=['condreg'],
            library_dirs=[os.path.join(condreg_cpp_dir, 'build')],
            runtime_library_dirs=[os.path.join(condreg_cpp_dir, 'build')],
            language='c++',
            extra_link_args=['-Wl,-rpath,{}'.format(os.path.join(condreg_cpp_dir, 'build'))]
        ),
    ]
else:
    ext_modules = []

setup(
    name='condreg_cpp',
    version=__version__,
    description='Python bindings for condreg-cpp',
    long_description='',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.4', 'numpy'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
    python_requires='>=3.6'
)
