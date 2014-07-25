# SECTOOL

A tool for for CI pipeline integration that is designed to check for security issues in web 
applications. 


##Dependencies
- virtualenv
- pip
- python3

##Install

###Dev 
```sh
pip3 install -r requirements.txt
python3 sectool.py ARGS
```

## Example Run

```sh
python3 sectool.py http://0.0.0.0:3000 EMAIL --auth admin@metacorp.com%admin1234
```
