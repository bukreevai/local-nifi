import argparse
from os import name

from .driver import Driver
from .config import (
    windows_config,
    unix_config
)

parser = argparse.ArgumentParser("scripts")
mutually_exclusive = parser.add_mutually_exclusive_group(required=True)
mutually_exclusive.add_argument("--up", action='store_true', help="Start local environmvent")
mutually_exclusive.add_argument("--down", action='store_true', help="Stop local environmvent")
args = parser.parse_args()

if name == 'nt':
    driver = Driver(windows_config)
else:
    driver = Driver(unix_config)

if args.up:
    driver.drive('up')
else: 
    driver.drive('down')

