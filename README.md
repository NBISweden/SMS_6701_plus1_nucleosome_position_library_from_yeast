# NBIS Support project 6701

- Last modified: ons mar 22, 2023  05:56
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

A script, [`create_sequence_tiles.py`](scripts/create_sequence_tiles.py), was
prepared for the task of generating sequence tiles covering plusone positions
and is available in the scripts folder. More instructions on how to use the
script are found in the [README.md](scripts/README.md) file in the scripts
folder.


### Input data

Two input files are required:

1. Genome file in fasta format:
   [Saccharomyces_cerevisiae_Ensembl_R64-1-1.tar.gz](http://igenomes.illumina.com.s3-website-us-east-1.amazonaws.com/Saccharomyces_cerevisiae/Ensembl/R64-1-1/Saccharomyces_cerevisiae_Ensembl_R64-1-1.tar.gz)
2. File with information on plusone positions:
   [GSE140614_+1coordiantesETC_tirosh_32U.tab.gz](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE140614&format=file&file=GSE140614%5F%2B1coordiantesETC%5Ftirosh%5F32U%2Etab%2Egz)

Examples on how to download and prepare the data are given in the
[README.md](data/README.md) file in the data folder.


### Output data from the script

The output data are tiled nt sequences of length `L`, covering a window size of
`W` centered on a plusone position `P` on the input genome, and with a tiling
step size of `S`.

The tiles are written as two sets: the first a direct copies of the genome, and
the second as reverse-complements of the first set.

The parameters `L`, `W`, and `S` can be altered by options in the script. The
positions `P` are read from the `plusonefile.tsv` file.


## Workflow example

Example of full workflow for preparing and generating data can be found in the
file [Notebook.md](Notebook.md).

