"""
git-phoenix setup.py
"""
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Package version
VERSION = "1.2.0"

setup(
    name="git-phoenix",
    version=VERSION,
    description="A dynamic git branching tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/victoraugustofd/git-phoenix",
    author="victoraugustofd",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "GitPython==3.1.24",
        "regex==2021.4.4",
        "argparse==1.4.0",
        "jsonschema==4.0.1",
        "coloredlogs==15.0.1",
        "questionary==1.10.0",
        "click==8.0.1",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "git-phoenix=src.git_phoenix:main",
            "git-px=src.git_phoenix:main",
        ]
    },
)
