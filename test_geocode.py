from geocode import geocode
import os


infile = "/home/luca/eodc/data/copernicus.eu/s1a_csar_grdh_iw/2016/08/03/S1A_IW_GRDH_1SDH_20160803T170701_20160803T170731_012439_0136C6_907F.zip"
outdir = os.getcwd() + "/snap_output"
externalDEMFile = "/home/luca/eodc/data/copernicus.eu/south_tyrol.tif"

bbox = {'xmin': 10.65, 'xmax': 10.55, 'ymin': 47.35, 'ymax': 47.45}
# out of bounds
#bbox = {'xmin': 4.65, 'xmax': 4.55, 'ymin': 17.35, 'ymax': 17.45}

_ = geocode(infile, outdir,
            shapefile=bbox,
            externalDEMFile=externalDEMFile,
            job_id='test-job')
