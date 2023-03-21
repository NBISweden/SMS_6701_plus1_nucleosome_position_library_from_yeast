# NBIS Support project 6701

- Last modified: tis mar 21, 2023  02:51
- Sign: Johan Nylander

## Description

> We would require your help in creating a DNA library for NGS sequencing with
> the following requirements. We will select a number (we need to discuss how
> many) of S. cerevisiae genes and find their previously published +1 nucleosome
> positions. Of these we would like you to create number of roughly 100-bp
> sequences that tile the genomic region around the +1 position with 7-bp
> increments and both orientations relative to the adapter sequences we insert at
> the ends. We will need to discuss the length of the region we want to tile, but
> it would be at least 300 bp. We obviously could do this manually, but I think
> with your bioinformatics expertise, it should be relatively easy to do this in
> a much more automatized and faster way.


## Input data

The script [`create_sequence_tiles.py`](scripts/create_sequence_tiles.py)
requires two input files: one genome file (nt sequences in fasta format), and
one plusone-file; a tab-separated file with chromosome labels, gene names, and
plusone positions.

Suggestions on how to prepare these files from published material can be found
in the [README.md](data/README.md) file inside the data folder.

## Script `create_sequence_tiles.py`

A script, [`create_sequence_tiles.py`](scripts/create_sequence_tiles.py), was
prepared for the task of generating sequence tiles covering plusone positions
and is available in the script folder.

To run the script, the [python interpreter](https://www.python.org/) needs to
installed together with the python library
[`pyfaidx`](https://pypi.org/project/pyfaidx/).

More instructions on how to use the script are found in the
[README.md](scripts/README.md) file in the scripts folder.

## Output data

The output data are tiled nt sequences of length `L`, covering a window size of
`W` centered on a plusone position `P` on the input genome, and with a tiling
step size of `S`.

The tiles are written as two sets: the first a direct copies of the genome, and
the second as reverse-complements of the first set.

The parameters `L`, `W`, and `S` can be altered by options in the script. The
positions `P` are read from the `plusonefile.tsv` file.

##  Testing on smaller data

    $ ./scripts/create_sequence_tiles.py -f data/chrI.fa -p data/chrI.tsv

