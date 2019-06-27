import os
import healpy as hp
import numpy as np
import file_verification as verif
from astropy.io import ascii, fits
from astropy.table import Table

def write_fits(table,params):
    file = "_".join(("PixelFit",str(params['NSIDE']),str(int(params['pixel']))))
    file = ".".join((file,"fits"))
    path = os.getcwd()
    path = os.path.join(path,"FITS")
    verif.file_verification(path,file,params['NSIDE'])
    path = os.path.join(path,str(params['NSIDE']))
    table.write(os.path.join(path,file))

    
def read_fit(params): 
    params['ang'] = hp.pix2ang(params['NSIDE'],int(params['pixel']), nest = True, lonlat=True)
    file_name     = "_".join(["PixelFit",str(params['NSIDE']),str(params['pixel'])])
    file_name     = ".".join([file_name,"fits"])
    
    tab = Table.read(os.path.join("FITS",str(params['NSIDE']),file_name))

    return tab, params
