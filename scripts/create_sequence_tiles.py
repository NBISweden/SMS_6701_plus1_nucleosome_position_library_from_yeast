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

    $ ./create_sequence_tiles.py -p plusonefile.tsv -f genome.fa

Options:

    -f, --fasta   FASTA fasta (genome) file
    -p, --plusone TSV plusone tsv file formatted as GSE140614_+1coordiantesETC_tirosh_32U.tab
    -P, --Plusone TSV plusone tsv file with chr strand name plus1
    -s, --step    STEPSIZE tile increment step size (default: 7)
    -l, --length  TILELENGTH length of tile (default: 100)
    -w, --window  WINDOWSIZE size of window (default: 350)
    -o, --output  OUTPUT Output file (default: standard output)
    -h, --help    Show this help message and exit
    -v, --verbose Increase output verbosity
    -V, --version Show program's version number and exit

Input:

    genome.fasta    Sequence (nt) file in fasta format
    plusonefile.tsv Tab-separated file with information on chromosome names,
                    strand, gene names, and plusone positions.
                    Labels must match the genome file.
                    Currently, two input formats are allowed (see -p, -P).

Prerequisites:

    Python (> v3.6), with python library pyfaidx.

    Installation: pip install pyfaidx

"""

import sys
import argparse
import csv
from pyfaidx import Fasta

__version__ = '0.1'

PLUSONE_COLUMNS_DEFAULT = (1, 4, 6, 11) # Format as in GSE140614_+1coordiantesETC_tirosh_32U.tab
PLUSONE_COLUMNS_SIMPLE =  (0, 1, 2, 3) # chr strand name plus1

TILE_LENGTH_DEFAULT = 100
TILE_STEP_DEFAULT = 7
WINDOW_SIZE_DEFAULT = 350
extension_default = round(WINDOW_SIZE_DEFAULT/2)

def do_parse(args):
    """
    Function for parsing
    """

    if args.length:
        tile_length = args.length
    else:
        tile_length = TILE_LENGTH_DEFAULT

    if args.step:
        step_size = args.step
    else:
        step_size = TILE_STEP_DEFAULT

    if args.window:
        extension = round(args.window/2)
    else:
        extension = extension_default

    if args.output:
        out_file = open(args.output, "w", encoding = "utf8")
        if args.verbose:
            print(f'Will write output to {args.output}', file = sys.stderr)
    else:
        if args.verbose:
            print('Will write output to standard out', file = sys.stderr)

    if args.Plusone:
        p_file = args.Plusone
        pos = PLUSONE_COLUMNS_SIMPLE
        if args.verbose:
            print('Assuming \'chr strand name plus1\' as columns in plusone file',
                    file = sys.stderr)
    else:
        p_file = args.plusone
        pos = PLUSONE_COLUMNS_DEFAULT

    genome = Fasta(args.fasta, sequence_always_upper = True)

    if args.verbose:
        print(f'Reading genome file {args.fasta}', file = sys.stderr)

    with open(p_file, "r", encoding = "utf8") as plusone_file:

        tsv_reader = csv.reader(plusone_file, delimiter = "\t")
        next(tsv_reader) # Skip the first row, which is assumed to be the header

        if args.verbose:
            print(f'Reading plusone file {p_file}', file = sys.stderr)

        for row in tsv_reader:
            (chrom, strand, name, plus1) = (row[pos[0]], row[pos[1]], row[pos[2]], row[pos[3]])

            if plus1 == 'NA':
                continue

            region_start = int(plus1) - extension
            region_stop = int(plus1) + extension
            region_seq = genome.get_seq(chrom, region_start, region_stop, rc = False).seq

            region_name = f">{chrom} {name} {strand} {plus1} {region_start}:{region_stop}"
            region_seq_rc = genome.get_seq(chrom, region_start, region_stop, rc = True).seq
            region_name_rc = f">{chrom} {name} {strand} {plus1} {region_start}:{region_stop} rc"

            if args.output:
                j = 0
                for i in range(0, len(region_seq) - tile_length + step_size, step_size):
                    print(f"{region_name} tile_{j}", file = out_file)
                    j = j + 1
                    print(region_seq[i: i + tile_length], file = out_file)
                j = 0
                for i in range(0, len(region_seq_rc) - tile_length + step_size, step_size):
                    print(f"{region_name_rc} tile_{j}", file = out_file)
                    j = j + 1
                    print(region_seq_rc[i: i + tile_length], file = out_file)
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

    if args.output:
        if not out_file.closed:
            out_file.close()

    if args.verbose:
        print('End of script', file = sys.stderr)

def main():
    """
    Check arguments, and run do_parse
    """
    if 0 in ((sys.version_info[0] == 3), (sys.version_info[1] >= 6)):
        print('Error: the script requires python v3.6 or higher')
        sys.exit(1)
    parser = argparse.ArgumentParser(
            prog = 'create_sequence_tiles',
            description = 'Parse genome file and plusone file',
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--fasta',
            required = True,
            type = str,
            help = 'fasta (genome) file')
    parser.add_argument('-l', '--length',
            type = int, nargs = '?', default = TILE_LENGTH_DEFAULT,
            help = 'length of tile')
    parser.add_argument('-s', '--step',
            type = int, nargs = '?', default = TILE_STEP_DEFAULT,
            help = 'tile increment step size')
    parser.add_argument('-w', '--window',
            type = int, nargs = '?', default = WINDOW_SIZE_DEFAULT,
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
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-p', '--plusone',
            type = str,
            help = 'TSV file formatted as GSE140614_+1coordiantesETC_tirosh_32U.tab')
    group.add_argument('-P', '--Plusone',
            type = str,
            help = 'TSV file with \'chr strand name plus1\'')
    parser.set_defaults(func = do_parse)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
