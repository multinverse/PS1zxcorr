#############################################################################################################
# This code was created by Alessandro Marins (University of Sao Paulo) and is owned by BINGO Telescope
#
# Its use is to extract optical data from Pan-STARRS1 telescope
#
# Any question about your operation, please, contact me in alessandro.marins@usp.br
#############################################################################################################

import os,sys,json
import argparse
import numpy as np
import healpy as hp
import query as qr
import galaxies_pixel as gal
import flags as fl
import strips as st
import write_read_fits as wr
import maxnside as mx
import file_verification as ver
from time import time,strftime, gmtime

###################################################################
# Check the python version and import configparser
###################################################################

if sys.version_info[0]==2:
    import ConfigParser
    config = ConfigParser.RawConfigParser()
	
elif sys.version_info[0]==3:
    import configparser
    config = configparser.ConfigParser()
	
###################################################################
# This part is for extracting information from parameters.ini file
###################################################################

name_params = os.path.join(os.getcwd(),"parameters_pixs.ini")
config.read(name_params)

user            = config.get(       "General","user_ps1")
pwd             = config.get(       "General","pwd_ps1")
nside           = config.getint(    "General","nside")
restart         = config.getboolean("General","restart")

use_constraint  = config.getboolean("Constraint","use")
type_constraint = config.get(       "Constraint","type")
band_constraint = config.get(       "Constraint","band")

use_flags       = config.getboolean("Flags","use")
table_flags     = config.getint(    "Flags","table")
band_flags      = config.get(       "Flags","band")
hex_flags       = config.get(       "Flags","hexadecimal")

try:
	pixels  = json.loads(config.get( "pixels_sky", "pixels"))
	for i in range(len(pixels)): 
		pixels[i]=int(pixels[i])
except:
	raise NameError

###############################################################################
#You can modify any options in the parameters.ini file by the command terminal
###############################################################################

parser = argparse.ArgumentParser(description='Modify by the command terminal parameters in parameters.ini file')

parser.add_argument('--user_ps1'       , action = 'store', dest = 'user'           , default = user           , help = '')
parser.add_argument('--pwd_ps1'        , action = 'store', dest = 'pwd'            , default = pwd            , help = '')
parser.add_argument('--nside'          , action = 'store', dest = 'nside'          , default = nside          , help = '')
parser.add_argument('--restart'        , action = 'store', dest = 'restart'        , default = restart        , help = '')

parser.add_argument('--use_constraint' , action = 'store', dest = 'use_constraint' , default = use_constraint , help = '')
parser.add_argument('--type_constraint', action = 'store', dest = 'type_constraint', default = type_constraint, help = '')
parser.add_argument('--band_constraint', action = 'store', dest = 'band_constraint', default = band_constraint, help = '')

parser.add_argument('--use_flags'      , action = 'store', dest = 'use_flags'      , default = use_flags      , help = '')
parser.add_argument('--table_flags'    , action = 'store', dest = 'table_flags'    , default = table_flags    , help = '')
parser.add_argument('--band_flags'     , action = 'store', dest = 'band_flags'     , default = band_flags     , help = '')
parser.add_argument('--hex_flags'      , action = 'store', dest = 'hex_flags'      , default = hex_flags      , help = '')

parser.add_argument('--pixels'         , action = 'store', dest = 'pixels'         , default = pixels         , nargs='+', type=int, help = '')

###############################################################################
#Variables
###############################################################################
arguments = parser.parse_args()

user            = str(arguments.user)
pwd             = str(arguments.pwd)
nside           = int(arguments.nside)
restart         = bool(arguments.restart)

use_constraint  = bool(arguments.use_constraint)
type_constraint = str(arguments.type_constraint)
band_constraint = str(arguments.band_constraint)

use_flags       = bool(arguments.use_flags)
table_flags     = int(arguments.table_flags)
band_flags      = str(arguments.band_flags)
hex_flags       = int(arguments.hex_flags,16)

pixels          = list(arguments.pixels)

###############################################################################
# inputs
###############################################################################

NSIDE          = nside
constraints    = {"use":use_constraint, "type":type_constraint, "band": band_constraint} 
params_flags   = {"use":use_flags, "table":table_flags, "band":band_flags}
hexa_query     = hex_flags

del nside, use_constraint, type_constraint, band_constraint, use_flags, table_flags,band_flags
###############################################################################
# Access PS1 server
###############################################################################

try: # Python 3.x
    from urllib.parse import quote as urlencode
    from urllib.request import urlretrieve
except ImportError:  # Python 2.x
    from urllib import pathname2url as urlencode
    from urllib import urlretrieve

try: # Python 3.x
    import http.client as httplib 
except ImportError:  # Python 2.x
    import httplib

import getpass
if not os.environ.get('CASJOBS_WSID'):
    os.environ['CASJOBS_WSID'] = user
if not os.environ.get('CASJOBS_PW'):
    os.environ['CASJOBS_PW'] = pwd

###############################################################################
# The program start here
###############################################################################
print("----> Starting PS1zxcorr code <----\n")
print("Calculating the maximum resolution that does not cause problems for your connection...")

NPIX                   = hp.nside2npix(NSIDE)
params                 = {"NSIDE":NSIDE, "NPIX":NPIX} 
params["NSIDE max"]    = 2**10#8*mx.maxnside(user,pwd)

print("Maximum resolution is NSIDE: {}\n".format(params['NSIDE max']))
print("You'll use")
print("NSIDE      : {}".format(params['NSIDE']))

strips = pixels
len_strips = len(strips)

print("\n\n")
time0 = time()
for num,pix in enumerate(strips):
	timei     = time()
	theta,phi = hp.pix2ang(params['NSIDE'],pix, lonlat=True, nest=False)
		
	params['pixel'] = pix
		
	if not ver.exist_or_not_file(params,restart):
		print(ver.exist_or_not_file(params,restart))
		tab, job        = qr.query_function(params, constraints)
		tab             = gal.galaxies_pixel(tab,params)
		tab             = fl.flags_constraints(tab,hexa_query,params_flags)
			
		timef           = strftime('%H:%M:%S', gmtime(time()-timei))
			
		print("Program's time (hh:mm:ss): {}".format(timef))
		print("Pixel {}".format(pix))
			
		if len(tab)>0: wr.write_fits(tab,params)
		else: print("Not save. 0 galaxies")
			
		print("\n\n")
	
print("End Programm: {0}".format(time0-time()))
