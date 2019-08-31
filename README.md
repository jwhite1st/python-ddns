# Python-DDNS

[![Build Status](https://travis-ci.com/jwhite1st/python-ddns.svg?branch=master)](https://travis-ci.com/jwhite1st/python-ddns) [![GitHub license](https://img.shields.io/github/license/jwhite1st/python-ddns?style=flat-square)](https://github.com/jwhite1st/python-ddns/blob/master/LICENSE.md)
![GitHub last commit](https://img.shields.io/github/last-commit/jwhite1st/python-ddns)![GitHub issues](https://img.shields.io/github/issues-raw/jwhite1st/python-ddns)

This is program written in python that acts as a DDNS client, currently just for Cloudflare.  
Works on python3 and up.  

I plan on making it a ppa to have it easier to update.

## To use

```bash
git clone https://github.com/jwhite1st/python-ddns
cd python-ddns/
pip install -r requirements
# Modify config.conf with the require fields.
# To test configuration
python3 python-ddns.py
# Edit crontab to run script
crontab -e
# Add
0 * * * * /usr/bin/python3 $PWD/python-ddns.py >/dev/null 2>&1 #Updates every hour.
```
