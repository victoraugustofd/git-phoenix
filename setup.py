"""
git-phoenix setup.py
"""
from setuptools import setup, find_packages

setup(
    name="git-phoenix",
    version="1.0.0",
    description="A dynamic git branching tool",
    author="victoraugustofd",
    url="https://github.com/victoraugustofd/git-phoenix",
    packages=find_packages(),
    entry_points={"console_scripts": ["git-phoenix=src.git_phoenix:main"]},
    install_requires=[
        "GitPython",
        "regex",
        "argparse",
        "jsonschema",
        "colorlog",
    ],
    python_requires="3.7",
    license="MIT",
)
