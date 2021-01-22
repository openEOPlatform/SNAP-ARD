from geocode import geocode
import sys

infile = sys.argv[1]
outdir = sys.argv[2]
shapefile = sys.argv[3]
externalDEMFile = sys.argv[4]

_ = geocode(infile, outdir,
            shapefile=shapefile,
            externalDEMFile=externalDEMFile)
