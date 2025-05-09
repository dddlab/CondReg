from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="condreg",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Condition number regularization for covariance matrices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/condreg-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "scikit-learn>=1.0.0"
    ],
)
