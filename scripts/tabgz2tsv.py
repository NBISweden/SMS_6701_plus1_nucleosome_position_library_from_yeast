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

       1      ID
    *  2      chr
       3      start
       4      end
    *  5      strand
       6      class
    *  7      name
       8      commonName
       9      endConfidence
      10      source
    * 11      plus1
      12      tss
      13      tts
      14      minus1
      15      plus1NK
      16      NFRcenter
      17      NFRlength
      18      lastNuc
      19      transcriptCenter
      20      centerNuc
      21      FirstToLastNucLength
      22      TSStoTTSLength
      23      dyadtodyadcenter
"""

import csv
import gzip

TABGZFILE = "GSE140614_+1coordiantesETC_tirosh_32U.tab.gz"
p = (1, 4, 6, 11) # chr strand name plus1 as in GSE140614_+1coordiantesETC_tirosh_32U.tab.gz

with open("simple.tsv", "w", encoding = "utf8") as outfile:
    with gzip.open(TABGZFILE, mode = "rt") as infile:
        tsv_reader = csv.reader(infile, delimiter = "\t")
        for row in tsv_reader:
            (chrom, strand, name, plus1) = (row[p[0]], row[p[1]], row[p[2]], row[p[3]])
            print(f"{chrom}\t{strand}\t{name}\t{plus1}", file = outfile)
