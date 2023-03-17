#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 nylander <johan.nylander@nrm.se>
#
# Distributed under terms of the MIT license.
#
# ./create_sequence_tiles.py -p chrI.tsv -f chrI.fasta

# TODO:
# - [ ] Print revcomp (genome['chrI'][200:230].complement) with correct info (change strand?) in header
#

"""
Description:

    Parse a genome and a plusone file, print fasta

Usage:

    text

Options:

    -f, --fasta FASTA fasta (genome) file
    -p, --plusone TSV plusone tsv file
    -s, --step STEPSIZE tile increment step size
    -l, --length TILELENGTH length of tile
    -w, --window WINDOWSIZE size of window
    -o, --output OUTPUT Output file (default: standard output)
    -h, --help show this help message and exit
    -v, --verbose increase output verbosity
    -V, --version show program's version number and exit

Examples:

    text

Prerequisites:

    text

"""

import sys
import re
import argparse
import csv
from pyfaidx import Fasta

__version__ = '0.1'
tile_length_default = 100
tile_step_default = 7
window_size_default = 350
extension_default = round(window_size_default/2)

# https://pythonhosted.org/pyfaidx/
#genome['chrI'][200:230].complement

def doParse(args):

    if (args.length):
        tile_length = args.length
    else:
        tile_length = tile_length_default

    if (args.step):
        step_size = args.step
    else:
        step_size = tile_step_default

    if (args.window):
        extension = round(args.window/2)
    else:
        extension = extension_default

    genome = Fasta(args.fasta, sequence_always_upper = True)

    with open(args.plusone, "r", encoding="utf8") as plusone_file:
        tsv_reader = csv.reader(plusone_file, delimiter="\t")
        next(tsv_reader) # Skip the first row, which is the header. Consider having this inside the loop

        for row in tsv_reader:
            # Variable assignments are highly dependent on exact (expected) input!
            (chrom, strand, name, plus1) = (row[1], row[4], row[6], row[11]) # TODO: Need to take care of 'NA' or ''?
            region_start = int(plus1) - extension
            region_stop = int(plus1) + extension
            region_seq = genome[chrom][region_start:region_stop].seq
            region_name = f">{chrom} {name} {strand} {plus1} {region_start}:{region_stop}"

            if (args.output):
                with open(args.output, 'w') as f:
                    j = 0
                    for i in range(0, len(region_seq) - tile_length + step_size, step_size):
                        print(f"{region_name} tile_{j}")
                        j = j + 1
                        print(region_seq[i: i + tile_length])
            else:
                #print(f"{region_name}")
                #print(f"{region_seq}")
                j = 0
                for i in range(0, len(region_seq) - tile_length + step_size, step_size):
                    print(f"{region_name} tile_{j}")
                    j = j + 1
                    print(region_seq[i: i + tile_length])

    if (args.verbose):
        print('\nEnd of script', file = sys.stderr)

def main():
    parser = argparse.ArgumentParser(
            prog = 'create_sequence_tiles',
            description = 'Parse genome file and plusone file',
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--fasta',
            required = True,
            type = str,
            help = 'fasta (genome) file')
    parser.add_argument('-p', '--plusone',
            required = True,
            type = str,
            help = 'Plusone file')
    parser.add_argument('-l', '--length',
            type = int, nargs = '?', default = tile_length_default,
            help = 'length of tile')
    parser.add_argument('-s', '--step',
            type = int, nargs = '?', default = tile_step_default,
            help = 'tile increment step size')
    parser.add_argument('-w', '--window',
            type = int, nargs = '?', default = window_size_default,
            help = 'window size')
    parser.add_argument('-o', '--output',
            type = str, nargs = '?',
            help = 'output file (default: standard output)')
    parser.add_argument('-v', '--verbose',
            action = 'store_true',
            help = 'increase output verbosity')
    parser.add_argument('-V', '--version',
            action = 'version',
            version = '%(prog)s version ' + __version__)
    parser.set_defaults(func = doParse)
    args = parser.parse_args()
    args.func(args)

if ( __name__ == "__main__"):
    main()

