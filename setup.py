"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/budgitree
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

# Load version string from package
from budgitree import __version__ as version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.

setup(
    name="budgitree",  # Required
    version=version,  # Required
    description="Budgitree newick tree processor",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/schultzm/budgitree",  # Optional
    author="Dr Mark B Schultz",  # Optional
    author_email="dr.mark.schultz@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="budgitree scientific exponential notation branch support decimal polytomy polytomies phylogenetic newick tree bifurcating",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    python_requires=">=3.7",
    install_requires=["ete3",
                      "biopython"],  # Optional
    extras_require={  # Optional
        "dev": ["pre-commit", "pipenv"],
        "test": ["pytest", "pytest-cov"],
    },
    package_data={"": ["*.tree"]},  # Optional
    entry_points={"console_scripts": ["budgitree = budgitree.__main__:main"]},  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/schultzm/budgitree/issues",
        "Source": "https://github.com/schultzm/budgitree/",
    },
)
