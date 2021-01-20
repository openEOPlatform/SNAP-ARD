from geocode import geocode
import os


infile = "S1A_IW_GRDH_1SDH_20160803T170701_20160803T170731_012439_0136C6_907F.zip"
outdir = os.getcwd() + "/snap_output"
externalDEMFile = os.getcwd() + "/south_tyrol.tif"

# equi7_wkt = 'PROJCS["Azimuthal_Equidistant",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Azimuthal_Equidistant"],PARAMETER["false_easting",5837287.81977],PARAMETER["false_northing",2121415.69617],PARAMETER["longitude_of_center",24.0],PARAMETER["latitude_of_center",53.0],UNIT["Meter",1.0]]''

# epsg = 32632
epsg = 3035  # ETRS89 Lambert Azimuthal Equal Area: https://epsg.io/3035
# http://mapref.org/LinkedDocuments/MapProjectionsForEurope-EUR-20120.pdf

_ = geocode(infile, outdir, t_srs=epsg, tr=10,
            shapefile={'xmin': 9.65, 'xmax': 13.77, 'ymin': 45.35, 'ymax': 47.78},
            externalDEMFile=externalDEMFile)
