import argparse
from os import name
import logging

from .driver import Driver
from .config import config

parser = argparse.ArgumentParser("scripts")
mutually_exclusive = parser.add_mutually_exclusive_group(required=True)
mutually_exclusive.add_argument("--up", action='store_true', help="Start local environmvent")
mutually_exclusive.add_argument("--down", action='store_true', help="Stop local environmvent")
parser.add_argument("--debug", action='store_true', help='Run in debug mode')

args = parser.parse_args()

log_level = logging.INFO

if args.debug:
    log_level = logging.DEBUG

logging.basicConfig(level = log_level, format = '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')

driver = Driver(config)

if args.up:
    driver.drive('up')
else: 
    driver.drive('down')

