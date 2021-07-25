# WebsiteProtocolTests

Runs different protocol tests on websites according to configuration

## Prerequisites 

- python3.8
- pip3.8

Or if you don't have python3.8 and pip3.8 installed:

- latest docker
- latest docker-compose

## Running instructions 

- clone the repository and `cd` into it
- install script's dependencies: `pip3.8 install -r requirements.txt`
- run the script `python3.8 main.py`

To see `DEBUG` messages run:

`python3.8 main.py --verbose`

## Testing instructions

`python3.8 -m unittest tests/utils_tests.py  tests/website_checks_tests.py`

## No python 3.8 installed? Run with docker and docker-compose

- clone the repository and `cd` into it
- `docker-compose up`
