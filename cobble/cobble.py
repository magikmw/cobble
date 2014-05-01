#! /bin/env python
# -*- coding: UTF-8 -*-

__doc__ = """Main file, parse arguments and run the program"""

"""This file is part of Cobble.

Cobble is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Cobble is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cobble; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import argparse # cli options and arguments parsing
import sys # exit()
import os # getcwd()

import generator
import util

__version__ = "Not Working At All"
_cli_description = "Yet Another Python Static Site Generator"

def version():
    """Print a version prompt"""
    print("cobble.py - static website/blog build script v." + __version__)
    print("Copyright (C) 2014 Michał Walczak <mw@michalwalczak.eu>")
    #[TODO] Add licensing info before giting

def parseopts():
    """Parse commandline arguments if any"""
    parser = argparse.ArgumentParser(description=_cli_description)
    parser.add_argument('-v', '--version', action='store_true',\
        help='print version and license information and quit')

    return parser.parse_args()

def main():
    """Act on the output of parseopts(), call the generator"""

    args = parseopts()
    print(args)

    if args.version:
        version() # if -v/--version is an option
        sys.exit()

    # check if the current folder holds all needed files
    # [TODO] Set this up so you can be artibrary with your project folder
    working_dir = os.getcwd()
    util.setup_dirs(working_dir)

    # build the site
    generator.generate_articles(util.abs_file_paths('articles'), working_dir)
    # generator.generate_blog()

if __name__ == '__main__':
    main()
