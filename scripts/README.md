# README create\_sequence\_tiles.py

- Last modified: mån mar 20, 2023  02:54
- Sign: JN

## Description:

Parse a genome and a plusone file, print fasta sequences representing
overlapping tiles covering a window centered at the plusone site.

## Usage:

    $ ./create_sequence_tiles.py -p plusonefile.tsv -f genome.fasta

## Options:

- `-f, --fasta`   FASTA fasta (genome) file
- `-p, --plusone` TSV plusone tsv file
- `-s, --step`    STEPSIZE tile increment step size (default: 7)
- `-l, --length`  TILELENGTH length of tile (default: 100)
- `-w, --window`  WINDOWSIZE size of window (default: 350)
- `-o, --output`  OUTPUT Output file (default: standard output)
- `-h, --help`    show this help message and exit
- `-v, --verbose` increase output verbosity
- `-V, --version` show program's version number and exit

## Input:

- `genome.fasta` Sequence (nt) file in fasta format
- `plusonefile.tsv` Tab-separated file with information on chromosome names,
  gene names, and plusone positions.  Labels must match the genome file.

## Prerequisites:

Python (> v3.6), with python library pyfaidx.

Installation: 

    $ pip install pyfaidx

