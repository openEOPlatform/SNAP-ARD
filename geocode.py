
from equi7grid import equi7grid
from equi7grid.image2equi7grid import image2equi7grid
from glob import glob
from osgeo.gdal import Translate
import os
from pyroSAR import snap
import requests
import shutil
import subprocess
import time
from uuid import uuid4


def geocode(infile, outdir, shapefile, externalDEMFile=None,
            refarea='gamma0', terrainFlattening=True, tmp_dir=None):

    start_time = time.time()
    identifier = os.path.splitext(os.path.split(infile)[1])[0]
    if not tmp_dir:
        tmp_dir = "/tmp/" + str(uuid4())
    tmp_dir_snap = tmp_dir + "/" + identifier
    os.makedirs(tmp_dir_snap, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)

    if externalDEMFile:
        # Crop DEM to bbox of infile
        externalDEMFile = crop_DEM(infile, externalDEMFile, tmp_dir_snap)

    epsg = 4326
    sampling = 10  # in meters

    _ = snap.geocode(infile=infile,
                     outdir=tmp_dir_snap,
                     refarea=refarea,
                     t_srs=epsg,
                     tr=sampling,
                     shapefile=shapefile,
                     externalDEMFile=externalDEMFile,
                     externalDEMApplyEGM=False,
                     terrainFlattening=terrainFlattening,
                     cleanup=True, allow_RES_OSV=True,
                     scaling='linear', groupsize=1, removeS1ThermalNoise=True
                     )
    # Move log file and SNAP xml file to outdir
    xml_file = glob(os.path.join(tmp_dir_snap, "*.xml"))[0]
    shutil.move(xml_file, xml_file.replace(tmp_dir_snap, outdir))
    orb_dir = os.path.basename(f"{xml_file}")[10].replace('A', 'ascending').replace('D', 'descending')
    e7 = equi7grid.Equi7Grid(sampling=10)
    file_list = glob(tmp_dir_snap + "/S1*.tif")
    for k, this_file in enumerate(file_list):
        # Ad polarization info to snap filename
        file_dir, filename = (os.path.dirname(this_file), os.path.basename(this_file))
        filename = filename[:28] + identifier[9] + filename[28:]
        this_file_new = os.path.join(file_dir, filename)
        shutil.move(this_file, this_file_new)
        this_file = this_file_new

        # Add metadata to geotiff headers
        subprocess.run(['gdal_edit.py',
                        '-mo', 'snap_version=7.0',
                        '-mo', f'snap_xml_graph={xml_file}',
                        '-mo', 'proc_facility=EODC-cloud',
                        '-mo', f'start_time={identifier[17:32]}',
                        '-mo', f'end_time={identifier[33:48]}',
                        '-mo', f'orbit_direction={orb_dir}',
                        this_file
                        ], capture_output=True)

        # Reproject and tile to EQUI7
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
    lry = float(low_corner.split(' ')[0])
    ulx = float(low_corner.split(' ')[1])
    up_corner = response.json()['csw:GetRecordByIdResponse']['csw:Record']['ows:BoundingBox']['ows:UpperCorner']
    uly = float(up_corner.split(' ')[0])
    lrx = float(up_corner.split(' ')[1])

    # Crop DEM
    out_dem_filepath = f"{tmp_dir}/cropped_DEM.tif"
    _ = Translate(out_dem_filepath, dem_filepath, projWin=(ulx, uly, lrx, lry))

    return out_dem_filepath
