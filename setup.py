import re
import os
import codecs

from setuptools import setup, find_packages

long_description = """Some projects such as Tito, Packit,
Fedora Review Service, etc operate over currently active Fedora releases.
They either need to manualy define them in a list or implement a code similar
to this."""

setup_requires = [
    "pytest",
    "munch",
]

install_requires = [
    "munch",
    "bodhi-client",
]

__description__ = "Aliases for active Fedora releases"
__author__ = "Copr and Packit teams"
__author_email__ = "copr-devel@lists.fedorahosted.org"
__url__ = "https://github.com/rpm-software-management/fedora-distro-aliases"


setup(
    name="fedora-distro-aliases",
    version="1.0",
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
