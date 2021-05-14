import ast
from geocode import geocode
import sys

infile = sys.argv[1]
outdir = sys.argv[2]
shapefile = sys.argv[3]
externalDEMFile = sys.argv[4]
tmpdir = sys.argv[5]
job_id = sys.argv[6]
job_id_vsc = sys.argv[7]
logdir = sys.argv[8]

if "{" in shapefile:
    # This is a dict, convert from str
    shapefile = ast.literal_eval(shapefile)

_ = geocode(infile, outdir,
            shapefile=shapefile,
            externalDEMFile=externalDEMFile,
            tmp_dir=tmpdir,
            job_id=job_id,
            job_id_vsc=job_id_vsc,
            logdir=logdir)
