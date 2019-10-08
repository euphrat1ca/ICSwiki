#!/usr/bin/env python3
"""Setup script for EXPLIoT."""
import os

from setuptools import find_packages, setup

import expliot.constants as expliot_const

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="expliot",
    version=expliot_const.__version__,
    url="https://expliot.io",
    license="AGPLv3+",
    author="Aseem Jakhar",
    author_email="aseemjakhar@gmail.com",
    description="Expliot - IoT security testing and exploitation framework",
    long_description=long_description,
    packages=find_packages(),
    entry_points={"console_scripts": ["expliot=expliot.expliot:EfCli.main"]},
    install_requires=[
        "bluepy>=1.1.4",
        "cmd2>=0.9.15",
        "coapthon3>=1.0.1",
        "paho-mqtt>=1.3.1",
        "pycrypto>=2.6.1",
        "pyi2cflash>=0.1.1",
        "pymodbus>=1.5.2",
        "pynetdicom>=1.2.0",
        "pyparsing>=2.2.0",
        "pyserial>=3.4",
        "pyspiflash>=0.5.2",
        "python-can>=2.1.0",
    ],
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English" "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Security",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Testing",
    ],
    keywords="IoT IIot security hacking expliot exploit framework",
)
