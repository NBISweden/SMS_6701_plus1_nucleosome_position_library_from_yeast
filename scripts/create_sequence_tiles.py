#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 nylander <johan.nylander@nbis.se>
#
# Distributed under terms of the MIT license.


"""
Description:

    Parse a genome and a plusone file, print fasta sequences
    representing overlapping tiles covering a window centered
    at the plusone site.

Usage:

    $ ./create_sequence_tiles.py -p plusonefile.tsv -f genome.fasta

Options:

    -f, --fasta   FASTA fasta (genome) file
    -p, --plusone TSV plusone tsv file
    -s, --step    STEPSIZE tile increment step size (default: 7)
    -l, --length  TILELENGTH length of tile (default: 100)
    -w, --window  WINDOWSIZE size of window (default: 350)
    -o, --output  OUTPUT Output file (default: standard output)
    -h, --help    show this help message and exit
    -v, --verbose increase output verbosity
    -V, --version show program's version number and exit

Input:

    genome.fasta    Sequence (nt) file in fasta format
    plusonefile.tsv Tab-separated file with information on chromosome names,
                    gene names, and plusone positions.
                    Labels must match the genome file.

Prerequisites:

    Python (> v3.6), with python library pyfaidx.

    Installation: pip install pyfaidx

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

    if (args.output):
        f = open(args.output, "w")
        if (args.verbose):
            print(f'Will write output to {args.output}', file = sys.stderr)

    genome = Fasta(args.fasta, sequence_always_upper = True)
    if (args.verbose):
        print(f'Reading genome file {args.fasta}', file = sys.stderr)

    with open(args.plusone, "r", encoding = "utf8") as plusone_file:

        tsv_reader = csv.reader(plusone_file, delimiter = "\t")
        next(tsv_reader) # Skip the first row, which is the header. Consider having this inside the loop

        if (args.verbose):
            print(f'Reading plusone file {args.plusone}', file = sys.stderr)

        for row in tsv_reader:
            # Note: Variable assignments are highly dependent on exact (expected) input!
            (chrom, strand, name, plus1) = (row[1], row[4], row[6], row[11])

            region_start = int(plus1) - extension
            region_stop = int(plus1) + extension
            region_seq = genome.get_seq(chrom, region_start, region_stop, rc = False).seq

            region_name = f">{chrom} {name} {strand} {plus1} {region_start}:{region_stop}"
            region_seq_rc = genome.get_seq(chrom, region_start, region_stop, rc = True).seq
            region_name_rc = f">{chrom} {name} {strand} {plus1} {region_start}:{region_stop} rc"

            if (args.output):
                j = 0
                for i in range(0, len(region_seq) - tile_length + step_size, step_size):
                    print(f"{region_name} tile_{j}", file = f)
                    j = j + 1
                    print(region_seq[i: i + tile_length], file = f)
                j = 0
                for i in range(0, len(region_seq_rc) - tile_length + step_size, step_size):
                    print(f"{region_name_rc} tile_{j}", file = f)
                    j = j + 1
                    print(region_seq_rc[i: i + tile_length], file = f)
            else:
                j = 0
                for i in range(0, len(region_seq) - tile_length + step_size, step_size):
                    print(f"{region_name} tile_{j}", file = sys.stdout)
                    j = j + 1
                    print(region_seq[i: i + tile_length], file = sys.stdout)
                j = 0
                for i in range(0, len(region_seq_rc) - tile_length + step_size, step_size):
                    print(f"{region_name_rc} tile_{j}", file = sys.stdout)
                    j = j + 1
                    print(region_seq_rc[i: i + tile_length], file = sys.stdout)

    if (args.output):
        if not f.closed:
            f.close()

    if (args.verbose):
        print('End of script', file = sys.stderr)

def main():
    if 0 in ((sys.version_info[0] == 3),  (sys.version_info[1] >= 6)):
        print('Error: the script requires python v3.6 or higher')
        exit(1)

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

