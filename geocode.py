
from equi7grid import equi7grid
from equi7grid.image2equi7grid import image2equi7grid
from glob import glob
import os
from pyroSAR import snap
import shutil


def geocode(infile, outdir, shapefile, externalDEMFile=None,
            refarea='gamma0', terrainFlattening=True):

    identifier = os.path.splitext(os.path.split(infile)[1])[0]
    tmp_dir = "/tmp/" + identifier
    os.makedirs(tmp_dir)

    # Use this projection for SNAP, before reprojectiing to EQUI7
    # Note: SNAP does not support EQUI7 yet
    epsg = 54032  # World Azimuthal Equidistant (https://epsg.io/54032)
    sampling = 10  # in meters

    _ = snap.geocode(infile=infile,
                     outdir=tmp_dir,
                     refarea=refarea,
                     t_srs=epsg,
                     tr=sampling,
                     shapefile=shapefile,
                     externalDEMFile=externalDEMFile,
                     terrainFlattening=terrainFlattening,
                     cleanup=True, allow_RES_OSV=True,
                     scaling='db', groupsize=1, removeS1ThermalNoise=True
                     )

    # Reproject and tile to EQUI7
    file_list = glob(tmp_dir + "/*.tif")
    e7 = equi7grid.Equi7Grid(sampling=10)
    for this_file in file_list:
        _ = image2equi7grid(e7, image=this_file,
                            output_dir=outdir,
                            gdal_path="/usr/bin")
    shutil.rmtree(tmp_dir)
