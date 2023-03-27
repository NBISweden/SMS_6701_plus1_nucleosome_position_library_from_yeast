# README.md

- Last modified: mån mar 27, 2023  05:04
- Sign: Johan Nylander


## Description

Prepare data for input to script.


### Genome

Should be the correct genome used according to Klaus Brackmann ons 22 mar 2023.
Need to correct the fasta headers in this version of the genome to match the plusone-file.
See also alternative genome file below.

    $ wget "http://igenomes.illumina.com.s3-website-us-east-1.amazonaws.com/Saccharomyces_cerevisiae/Ensembl/R64-1-1/Saccharomyces_cerevisiae_Ensembl_R64-1-1.tar.gz"
    $ tar --strip-components 5 -xf Saccharomyces_cerevisiae_Ensembl_R64-1-1.tar.gz Saccharomyces_cerevisiae/Ensembl/R64-1-1/Sequence/WholeGenomeFasta/genome.fa
    $ sed -i '/>/ s/>/>chr/' genome.fa

**Alternative**: Use the UCSC sacCer3 genome (has the same fasta headers as the GSE140614-file)

    $ wget "http://igenomes.illumina.com.s3-website-us-east-1.amazonaws.com/Saccharomyces_cerevisiae/UCSC/sacCer3/Saccharomyces_cerevisiae_UCSC_sacCer3.tar.gz"
    $ tar --strip-components 5 -xf Saccharomyces_cerevisiae_UCSC_sacCer3.tar.gz  Saccharomyces_cerevisiae/UCSC/sacCer3/Sequence/WholeGenomeFasta/genome.fa


### Plusone file

    $ wget -O GSE140614_+1coordiantesETC_tirosh_32U.tab.gz \
          "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE140614&format=file&file=GSE140614%5F%2B1coordiantesETC%5Ftirosh%5F32U%2Etab%2Egz"

Header labels in the `GSE140614_+1coordiantesETC_tirosh_32U.tab.gz` file.
The ones with an asterisk are selected.

    $ gunzip -c GSE140614_+1coordiantesETC_tirosh_32U.tab.gz | head -1 | tr '\t' '\n' | nl
         1	ID
      *  2	chr
         3	start
         4	end
      *  5	strand
         6	class
      *  7	name
         8	commonName
         9	endConfidence
        10	source
      * 11	plus1
        12	tss
        13	tts
        14	minus1
        15	plus1NK
        16	NFRcenter
        17	NFRlength
        18	lastNuc
        19	transcriptCenter
        20	centerNuc
        21	FirstToLastNucLength
        22	TSStoTTSLength
        23	dyadtodyadcenter

Create the `plusonefile.tsv` file (using gunzip and awk. Note that column numbering starts at 1)

    $ gunzip -c GSE140614_+1coordiantesETC_tirosh_32U.tab.gz | \
          awk -v FS='\t' -v OFS='\t' '{print $2, $5, $7, $11}' > plusonefile.tsv

As an alternative, the python script [`tabgz2tsv.py`](../scripts/tabgz2tsv.py)
can be used for the creation of a simpler tsv file (output named `simple.tsv`).
See the [README.md](../scripts/README.md) in the scripts folder for description.

