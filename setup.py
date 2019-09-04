# pylint: disable=invalid-name, missing-docstring, line-too-long
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="Python DDNS",
    version="0.0.1",
    author="Jacob White",
    author_email="jake@jwhite.network",
    install_requires=['requests'],
    package_data={'config': ['.conf']},
    description="A DDNS client written in python that updates the A record on Cloudflare with the current IP of this device.",
    url="https://gitlab.com/jwhite1st/python-ddns",
    project_urls={
        "Issues": "https://gitlab.com/jwhite1st/python-ddns/issues",
    },
    license='GPL-3.0',
    packages=['python-ddns'],
    python_requires='>=3.6',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Installation/Setup",
        "Development Status :: 2 - Pre-Alpha"
    ],
    long_description=read('README.md'),
)
