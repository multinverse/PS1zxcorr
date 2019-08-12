import numpy as np
import healpy as hp

def range_dec(params):
    if params['dec strips']:
        return params['dec center'] - params['dec width']/2.,params['dec center'] + params['dec width']/2.
    else:
        return [-90.,90.]
    
def pixelstrips(params):
    dec1,dec0 = range_dec(params)
    
    nside     = params['NSIDE']
    theta_min = np.array(dec2col(dec1))
    theta_max = np.array(dec2col(dec0))
    pix = []
    if theta_min.size==1:
        pix = np.append(pix,hp.query_strip(nside,theta_max,theta_min, inclusive=True))
    else:
        for i in range(theta_min.size):
            pix = np.append(pix,hp.query_strip(nside,theta_max[i],theta_min[i], inclusive=True))
    return pix.astype(int)

def col2dec(colat=None, deg_out=False):
    colat = np.array(colat)
    ones  = np.ones(colat.size)
    
    down = np.where(colat<0)[0]
    up   = np.where(colat>180)[0]
    
    if (down.size+up.size)==0:
        if deg_out:
            return -(colat - 90.)
        else:
            return np.radians(-(colat - 90.))
    else: print("Error")
        
def dec2col(dec=None, deg_out=False):
    dec  = np.array(dec)
    ones = np.ones(dec.size)
    
    down = np.where(dec<-90.)[0]
    up   = np.where(dec>90.)[0]
    
    if (down.size+up.size)==0:
        if deg_out:
            return -(dec - 90.)
        else:
            return np.radians(-(dec - 90.))
    else: 
        print("Error")

def newtrips(strips,pix):
	
	wispix = np.where(strips==pix)[0] #wispix = where is pix?
	wispix = int(wispix)
	return strips[wispix:]
