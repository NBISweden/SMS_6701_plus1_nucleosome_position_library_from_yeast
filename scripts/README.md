# Scripts

- Last modified: tis mar 21, 2023  02:47
- Sign: JN

## Script create\_sequence\_tiles.py

### Description

Parse a genome and a plusone file, print fasta sequences representing
overlapping tiles covering a window centered at the plusone site.

### Usage

    $ ./create_sequence_tiles.py -p plusonefile.tsv -f genome.fa

### Options

- `-f, --fasta`   FASTA fasta (genome) file
- `-p, --plusone` TSV plusone tsv file formatted as GSE140614_+1coordiantesETC_tirosh_32U.tab
- `-P, --Plusone` TSV plusone tsv file with chr strand name plus1
- `-s, --step`    STEPSIZE tile increment step size (default: 7)
- `-l, --length`  TILELENGTH length of tile (default: 100)
- `-w, --window`  WINDOWSIZE size of window (default: 350)
- `-o, --output`  OUTPUT Output file (default: standard output)
- `-h, --help`    Show this help message and exit
- `-v, --verbose` Increase output verbosity
- `-V, --version` Show program's version number and exit

### Input

- `genome.fasta` Sequence (nt) file in fasta format.
- `plusonefile.tsv` Tab-separated file with information on chromosome names,
  strand, gene names, and plusone positions.  Labels must match the genome
  file.  Currently, two input formats are allowed (see -p, -P).

### Prerequisites

[Python](https://www.python.org/) (> v3.6), with python library [pyfaidx](https://pypi.org/project/pyfaidx/).

### License and Copyright

Distributed under terms of the [MIT license](LICENSE).

---

## Script tabgz2tsv.py

### Description

A script to convert the format in (the compressed) file `GSE140614_+1coordiantesETC_tirosh_32U.tab.gz`
to a simpler format by extracting columns `chr`, `strand`, `name`, `plus1`.

### Input

The script assumes that the (compressed) file `GSE140614_+1coordiantesETC_tirosh_32U.tab.gz` is in the
same directory as the script.

### Output

The script writes to a file `simple.tsv`.


