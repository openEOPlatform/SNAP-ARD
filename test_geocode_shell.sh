#!/bin/bash

INFILE=/home/luca/eodc/data/copernicus.eu/s1a_csar_grdh_iw/2016/08/03/S1A_IW_GRDH_1SDH_20160803T170701_20160803T170731_012439_0136C6_907F.zip
OUTDIR=/home/luca/eodc/repos/openeo/SNAP-ARD/snap_output2
SHAPEFILE="{'xmin':9.65,'xmax':13.77,'ymin':45.35,'ymax':47.78}"
EXTERNALDEMFILE=/home/luca/eodc/repos/openeo/SNAP-ARD/south_tyrol.tif

python3 geocode_shell.py $INFILE $OUTDIR $SHAPEFILE $EXTERNALDEMFILE
