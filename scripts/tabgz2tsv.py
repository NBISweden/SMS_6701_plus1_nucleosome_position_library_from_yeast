#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 nylander <johan.nylander@nbis.se>
#
# Distributed under terms of the MIT license.

"""
Convert GSE140614_+1coordiantesETC_tirosh_32U.tab.gz to simpler
format (chr strand name plus1). Columns with an asterisk are
selected (including header)

       0      ID
    *  1      chr
       2      start
       3      end
    *  4      strand
       5      class
    *  6      name
       7      commonName
       8      endConfidence
       9      source
    * 10      plus1
      11      tss
      12      tts
      13      minus1
      14      plus1NK
      15      NFRcenter
      16      NFRlength
      17      lastNuc
      18      transcriptCenter
      19      centerNuc
      20      FirstToLastNucLength
      21      TSStoTTSLength
      22      dyadtodyadcenter
"""

import csv
import gzip

TABGZFILE = "GSE140614_+1coordiantesETC_tirosh_32U.tab.gz"
p = (1, 4, 6, 10) # chr strand name plus1 as in GSE140614_+1coordiantesETC_tirosh_32U.tab.gz

with open("simple.tsv", "w", encoding = "utf8") as outfile:
    with gzip.open(TABGZFILE, mode = "rt") as infile:
        tsv_reader = csv.reader(infile, delimiter = "\t")
        for row in tsv_reader:
            (chrom, strand, name, plus1) = (row[p[0]], row[p[1]], row[p[2]], row[p[3]])
            print(f"{chrom}\t{strand}\t{name}\t{plus1}", file = outfile)
