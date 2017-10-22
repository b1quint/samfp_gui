---
layout: single
permalink: /docs/
title: "Using SAM-FP"
author_profile: false
---

## Running the Scripts

### xjoin

The images acquired with SAM-FP come from SAMI, the SAM Imager. This instrument provides FITS files with four extensions. We first combine all the extensions using the script `xjoin`. This will create a copy of the original file with a prefix `xj_`. You may add other options when combining the extensions like removing cosmic rays using LACosmic adding the `-r` or cleaning known bad columns when observing with binning mode 4 x 4 pixels with the `-c` flat. These flags are also added to the prefix.

BIAS images can also be subtracted from the image that is being processed using a `-b` flat and giving the name of the master bias file to the program.

FLAT corrections can also be applied by provinding the `-f` flag and the master flat filename.

### combine_zero

TBD

### combine_flat

TBD

### phmxtractor

TBD

### phmfit

TBD

### phmapply

TBD

### fpwcal

TBD

### fpxmap

TBD
