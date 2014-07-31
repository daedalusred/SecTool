# SECTOOL

A tool for Continuous Integration pipeline integration that is designed to check for security issues in web
applications.  Wapiti (http://wapiti.sourceforge.net/) is the vulnerability scanner that SecTool currently supports.


##Dependencies
- virtualenv
- pip
- python3

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
python3 sectool.py http://0.0.0.0:3000 test@test.com --checkers xss,sql,backup,file,exec --auth admin@metacorp.com%admin1234 --format json --plugins wapiti
```

This will run wapiti and return a report in json format.
