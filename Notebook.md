# Notebook

- Last modified: mån mar 27, 2023  05:03
- Sign: Johan Nylander


## Description

Workflow for generating the plusone tiles.

See [Requirements](#requirements) for software used.


## Workflow

### Setup

    $ pip install pyfaidx # needed for create_sequence_tiles.py

    $ git clone https://github.com/NBISweden/SMS_6701_plus1_nucleosome_position_library_from_yeast.git
    $ cd SMS_6701_plus1_nucleosome_position_library_from_yeast
    $ mkdir -p run/{chroms,genes,chroms-genes}
    $ cd run


### Download plusone data, and replace parantheses in gene names with underscores

    $ wget -O GSE140614_+1coordiantesETC_tirosh_32U.tab.gz \
        "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE140614&format=file&file=GSE140614%5F%2B1coordiantesETC%5Ftirosh%5F32U%2Etab%2Egz"
    $ gunzip -c GSE140614_+1coordiantesETC_tirosh_32U.tab.gz |
        awk -v FS='\t' -v OFS='\t' '{print $2, $5, $7, $11}' > plusonefile.tsv
    $ sed -i 's/[(|)]/_/g' plusonefile.tsv


### Download genome data

Should be the correct genome used according to Klaus Brackmann ons 22 mar 2023.
Need to correct the fasta headers in this version of the genome to match the plusone-file.
See also description of alternative genome file in [data/README.md](data/README.md) .

    $ wget "http://igenomes.illumina.com.s3-website-us-east-1.amazonaws.com/Saccharomyces_cerevisiae/Ensembl/R64-1-1/Saccharomyces_cerevisiae_Ensembl_R64-1-1.tar.gz"
    $ tar --strip-components 5 -xf Saccharomyces_cerevisiae_Ensembl_R64-1-1.tar.gz Saccharomyces_cerevisiae/Ensembl/R64-1-1/Sequence/WholeGenomeFasta/genome.fa
    $ sed -i '/>/ s/>/>chr/' genome.fa


### Create tiles

Note the capital `-P` argument when using the format in the GSE140614 file

    $ ../scripts/create_sequence_tiles.py -f genome.fa -P plusonefile.tsv -o outfile.fas


### Convert to tab

    $ ../scripts/fasta2tab outfile.fas > outfile.tsv


### Get unique chromosomes:

    $ awk '{print $1}' outfile.tsv | sort -u > chroms/chroms.txt


### Extract chromosome-specific sequences

    $ cat chroms/chroms.txt | \
        parallel 'grep -w {} outfile.tsv | ../scripts/tab2fasta > chroms/{}.fas'


### Get gene names

Note: some of the names can be lists (e.g. `YOR008W-B, YOR009W`)

    $ perl -ne 'if (/^\S+\s([\S\s]+)\s[+-]/) {print "$1\n"}' outfile.tsv | \
        sort -u > genes/genes.txt


### Extract genes

    $ do_grep() {
        string="$1"
        fname="${string//, /_}"
        rex=
        rex="[^,][[:space:]]$string[[:space:]]" # hack using the [^,]
        grep -E "$rex" outfile.tsv | ../scripts/tab2fasta > genes/"$fname".fas
    }
    $ export -f do_grep
    $ cat genes/genes.txt | parallel do_grep "{}"


Note: Some genes seems to have more than one plusone position:

    YDL154W
    YGR067C
    YIL057C
    YKR097W
    YML042W
    YOL011W
    YOL045W
    YOR003W
    YOR328W
    YPL147W
    YPR006C


### Sort on both chromomose and gene

    $ for f in chroms/*.fas ; do
        c=$(basename "$f" .fas)
        echo "$c"
        mkdir -p chroms-genes/"$c"
        cp $(grep -w -l "$c" genes/*.fas) chroms-genes/"$c"/
      done


### Clean up (remove) some files

    $ rm genome.fa.fai GSE140614_+1coordiantesETC_tirosh_32U.tab.gz Saccharomyces_cerevisiae_Ensembl_R64-1-1.tar.gz


### Package (compress) run folder (25 MB)

    $ cd ..
    $ mv run NBIS_SMS_6701_data
    $ tar czf NBIS_SMS_6701_data.tgz NBIS_SMS_6701_data


## Requirements

All analyses was run on Linux operating system (Ubuntu 20.04). In addition to
standard shell (bash) commands, including python and perl, the following
software was used

- `git` <https://git-scm.com/>
- `parallel` <https://www.gnu.org/software/parallel/>
- `fasta2tab`, `tab2fasta` <https://github.com/nylander/fasta-tab>

