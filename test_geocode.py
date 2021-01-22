from geocode import geocode
import os


infile = "S1A_IW_GRDH_1SDH_20160803T170701_20160803T170731_012439_0136C6_907F.zip"
outdir = os.getcwd() + "/snap_output"
externalDEMFile = os.getcwd() + "/south_tyrol.tif"

_ = geocode(infile, outdir,
            shapefile={'xmin': 9.65, 'xmax': 13.77, 'ymin': 45.35, 'ymax': 47.78},
            externalDEMFile=externalDEMFile)
