"""
git-phoenix setup.py
"""
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="git-phoenix",
    version="1.0.4",
    description="A dynamic git branching tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/victoraugustofd/git-phoenix",
    author="victoraugustofd",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "GitPython",
        "regex",
        "argparse",
        "jsonschema==4.0.1",
        "coloredlogs",
        "questionary",
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
