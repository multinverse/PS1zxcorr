import os
import healpy as hp
import numpy as np
import file_verification as verif
from astropy.io import ascii, fits
from astropy.table import Table

def write_fits(table,params):
	str_npix      = str(params['NPIX'])
	str_nside     = str(params['NSIDE'])
	str_pix       = str(int(params['pixel']))
	len_str_npix  = len(str_npix)
	len_str_pix   = len(str_pix)
	len_zero      = len_str_npix - len_str_pix
	file_ = "_".join(("PixelFit",str_nside,"0"*len_zero+str_pix))
	file_ = ".".join((file_,"fits"))
	path = os.getcwd()
	path = os.path.join(path,"FITS")
	verif.file_verification(path,file_,params['NSIDE'])
	path = os.path.join(path,str(params['NSIDE']))
	table.write(os.path.join(path,file_))
	#file = "_".join(("PixelFit",str(params['NSIDE']),str(int(params['pixel']))))

    
def read_fit(params): 
	str_npix      = str(params['NPIX'])
	str_nside     = str(params['NSIDE'])
	str_pix       = str(int(params['pixel']))
	len_str_npix  = len(str_npix)
	len_str_pix   = len(str_pix)
	len_zero      = len_str_npix - len_str_pix
	file_ = "_".join(("PixelFit",str_nside,"0"*len_zero+str_pix))
	params['ang'] = hp.pix2ang(params['NSIDE'],int(params['pixel']), nest = True, lonlat=True)
	file_ = ".".join([file_,"fits"])
	tab = Table.read(os.path.join("FITS",str(params['NSIDE']),file_name))
	return tab, params
#file = "_".join(("PixelFit",str(params['NSIDE']),str(int(params['pixel']))))
#file_ = "_".join(["PixelFit",str(params['NSIDE']),str(params['pixel'])])
    
    
