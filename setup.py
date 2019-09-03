# pylint: disable=invalid-name, missing-docstring, line-too-long
from setuptools import setup

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
    license='MIT',
    packages=['python-ddns']

)
