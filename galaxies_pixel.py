import numpy as np
import healpy as hp


def galaxies_pixel(table,params):
    list1 = np.where(hp.ang2pix(params['NSIDE'],table['gra'],table['gdec'], lonlat=True) == params['pixel'])
    tab   = table[list1]
    print("Number of galaxies: {}".format(len(tab)))
    return  tab
