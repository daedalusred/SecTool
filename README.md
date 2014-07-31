# SECTOOL

A tool for Continuous Integration pipeline integration that is designed to check for security issues in web
applications.  Wapiti (http://wapiti.sourceforge.net/) is the vulnerability scanner that SecTool currently supports.


##Dependencies
- virtualenv
- pip
- python 2.7+ / python 3.3+

##Install

###Development
```sh
virtualenv .env
source .env/bin/activate
pip3 install -r requirements.txt
python3 sectool.py ARGS
```

## Example Run

```sh
python sectool.py http://0.0.0.0:3000 EMAIL --auth admin@metacorp.com%admin1234
```
