import re
import os
import codecs

from setuptools import setup, find_packages

long_description = """Some projects such as Tito, Packit,
Fedora Review Service, etc operate over currently active Fedora releases.
They can use this package to find their version numbers instead of manually
defining a list.

This package queries Bodhi to find the active releases and therefore requires an
internet connection."""

setup_requires = [
    "pytest",
    "munch",
]

install_requires = [
    "munch",
    "requests",
]

__description__ = "Aliases for active Fedora releases"
__author__ = "Copr and Packit teams"
__author_email__ = "copr-devel@lists.fedorahosted.org"
__url__ = "https://github.com/rpm-software-management/fedora-distro-aliases"


setup(
    name="fedora-distro-aliases",
    version="1.1",
    description=__description__,
    long_description=long_description,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license="GPLv2+",
    classifiers=[],
    setup_requires=setup_requires,
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
