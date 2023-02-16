#!/usr/bin/env python
'''
Load legacy processed and auv-python processed Dorado data for comparison

Mike McCann
MBARI 29 September 2022
'''

import os
import sys
from datetime import datetime

parentDir = os.path.join(os.path.dirname(__file__), "../")
sys.path.insert(0, parentDir)  # So that CANON is found

from CANON import CANONLoader
import timing

cl = CANONLoader('stoqs_auv_compare', 'Compare legacy and auv-python processed Dorado data',
                 description='Variables from Matlab & auv-python processing loaded together for visual comparison in the STOQS UI',
                 x3dTerrains={
                   'https://stoqs.mbari.org/x3d/Monterey25_10x/Monterey25_10x_scene.x3d': {
                     'position': '-2822317.31255 -4438600.53640 3786150.85474',
                     'orientation': '0.89575 -0.31076 -0.31791 1.63772',
                     'centerOfRotation': '-2711557.9403829873 -4331414.329506527 3801353.4691465236',
                     'VerticalExaggeration': '10',
                   },
                   'https://stoqs.mbari.org/x3d/Monterey25_1x/Monterey25_1x_src_scene.x3d': {
                     'name': 'Monterey25_1x',
                     'position': '-2822317.31255 -4438600.53640 3786150.85474',
                     'orientation': '0.89575 -0.31076 -0.31791 1.63772',
                     'centerOfRotation': '-2711557.9403829873 -4331414.329506527 3801353.4691465236',
                     'VerticalExaggeration': '1',
                   },
                 },
                 grdTerrain=os.path.join(parentDir, 'Monterey25.grd')
                 )

# Monterey Bay overnight diamond runs
startdate = datetime(2016, 6, 5)
enddate = datetime.utcnow()
# The first nighttime Diamond misssion - Temporal: 2016-06-27 14:56:41 to 2016-06-28 07:55:37
##startdate = datetime(2016, 6, 29)
##enddate = datetime(2016, 7, 2)

# Execute the load
cl.process_command_line()
if cl.args.test:
    cl.stride = 1000

cl.loadDorado(startdate, enddate, build_attrs=True, file_patterns=(r".*netcdf/dorado_.*1S.nc", ), title_match="Monterey Bay Diamond")
cl.loadDorado(startdate, enddate, build_attrs=True, file_patterns=(r".*_decim.nc$", ), plankton_proxies=True)

# Add any X3D Terrain information specified in the constructor to the database - must be done after a load is executed
cl.addTerrainResources()

print("All Done.")

