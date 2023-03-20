# NBIS Support project 6701

- Last modified: mån mar 20, 2023  02:45
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

## Script `create_sequence_tiles.py`

Script [`create_sequence_tiles.py`](scripts/create_sequence_tiles.py)
requires two input files: one genome file (nt sequences in fasta format),
and one plusone-file; a tab-separated file with chromosome labels,
gene names, and plusone positions.



