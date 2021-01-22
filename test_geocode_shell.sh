#!/bin/bash

INFILE=S1A_IW_GRDH_1SDH_20160803T170701_20160803T170731_012439_0136C6_907F.zip
OUTDIR=/path/to/outputdir
SHAPEFILE="{'xmin':9.65,'xmax':13.77,'ymin':45.35,'ymax':47.78}"
EXTERNALDEMFILE=/path/to/south_tyrol.tif

python3 geocode_shell.py $INFILE $OUTDIR $SHAPEFILE $EXTERNALDEMFILE
