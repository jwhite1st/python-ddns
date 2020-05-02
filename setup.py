"""Sets up Python-DDNS to be installed"""
import os
from setuptools import setup, find_packages
from pddns import __version__


def read(fname):
    """Reads README.md as long description"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="python-ddns",
    version=__version__,
    author="Cyb3r Jak3",
    author_email="jake@jwhite.network",
    install_requires=['requests'],
    description="A DDNS client that updates with current IP. "
                "Currently only Cloudflare and Hurricane Electric are supported.",  # noqa: E501 pylint: disable=line-too-long
    url="https://gitlab.com/Cyb3r-Jak3/python-ddns",
    project_urls={
        "Issues": "https://gitlab.com/Cyb3r-Jak3/python-ddns/issues",
        "Source": "https://gitlab.com/Cyb3r-Jak3/python-ddns"
    },
    data_files=[("config.conf", ["pddns/config.dist.conf"])],
    license='GPL-3.0',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Installation/Setup",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators"
    ],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    entry_points={
        "console_scripts": ['pddns=pddns.pddns:run']
    }
)
