
from equi7grid import equi7grid
from equi7grid.image2equi7grid import image2equi7grid
from glob import glob
from osgeo.gdal import Warp
import os
from pyroSAR import snap
import requests
import shutil
import time
from uuid import uuid4


def geocode(infile, outdir, shapefile, externalDEMFile=None,
            refarea='gamma0', terrainFlattening=True, tmp_dir=None):

    start_time = time.time()
    identifier = os.path.splitext(os.path.split(infile)[1])[0]
    if not tmp_dir:
        tmp_dir = "/tmp/" + str(uuid4())
    tmp_dir_snap = tmp_dir + "/" + identifier
    os.makedirs(tmp_dir_snap)

    if externalDEMFile:
        # Crop DEM to bbox of infile
        externalDEMFile = crop_DEM(infile, externalDEMFile, tmp_dir)

    epsg = 4326
    sampling = 10  # in meters

    _ = snap.geocode(infile=infile,
                     outdir=tmp_dir_snap,
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

    proc_time = time.time() - start_time
    minutes = round(proc_time / 60)
    seconds = round(((proc_time / 60) - minutes) * 60)
    print("Processing time: {mins} minutes and {secs} seconds.".format(mins=str(minutes), secs=str(seconds)))


def crop_DEM(infile, dem_filepath, tmp_dir):
    """ Crop DEM according to bbox of input file."""

    # Get bbox of infile
    csw_url = ("https://csw.eodc.eu/csw?service=CSW&version=2.0.2&request="
               "GetRecordById&ElementSetName=full&outputSchema="
               "http://www.opengis.net/cat/csw/2.0.2&id="
               )
    id = os.path.basename(infile).split('.zip')[0]
    response = requests.get(f"{csw_url}{id}&outputFormat=application/json")
    low_corner = response.json()['csw:GetRecordByIdResponse']['csw:Record']['ows:BoundingBox']['ows:LowerCorner']
    minY = float(low_corner.split(' ')[0])
    minX = float(low_corner.split(' ')[1])
    up_corner = response.json()['csw:GetRecordByIdResponse']['csw:Record']['ows:BoundingBox']['ows:UpperCorner']
    maxY = float(up_corner.split(' ')[0])
    maxX = float(up_corner.split(' ')[1])

    # Crop DEM
    out_dem_filepath = f"{tmp_dir}/cropped_DEM.tif"
    _ = Warp(out_dem_filepath, dem_filepath, outputBounds=(minX, minY, maxX, maxY))

    return out_dem_filepath
