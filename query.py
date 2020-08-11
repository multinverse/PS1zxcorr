import mastcasjobs
import healpy as hp
import numpy as np
import requests
import os, sys, re
import json
from astropy.io import ascii, fits
from astropy.table import Table, join, hstack, vstack


def parameters(nside,pixel):
    radius = hp.pixelfunc.max_pixrad(nside, degrees=True)*3600
    angles = hp.pix2ang(nside,int(pixel), nest = False, lonlat=True)
    return angles, radius
    
    
def fixcolnames(tab):
    """Fix column names returned by the casjobs query
    
    Parameters
    ----------
    tab (astropy.table.Table): Input table

    Returns reference to original table with column names modified"""

    pat = re.compile(r'\[(?P<name>[^[]+)\]')
    for c in tab.colnames:
        m = pat.match(c)
        if not m:
            raise ValueError("Unable to parse column name '{}'".format(c))
        newname = m.group('name')
        tab.rename_column(c,newname)
    return tab

def query_string(ang0,ang1,radius):
    query = """select sot.objID, sot.uniquePspsSTid, sot.ippObjID, sot.surveyID, sot.tessID, sot.projectionID, sot.skyCellID, sot.randomStackObjID, sot.primaryDetection, sot.bestDetection, sot.dvoRegionID, sot.processingVersion,
 sot.gippDetectID, sot.gstackDetectID, sot.gstackImageId, sot.gra, sot.gdec, sot.graErr, sot.gdecErr, sot.gEpoch, sot.gPSFMag, sot.gPSFMagErr, sot.gApMag, sot.gApMagErr, sot.gKronMag, sot.gKronMagErr, sot.ginfoFlag, sot.ginfoFlag2, sot.ginfoFlag3, sot.gnFrames,
 sot.rippDetectID, sot.rstackDetectID, sot.rstackImageId, sot.rra, sot.rdec, sot.rraErr, sot.rdecErr, sot.rEpoch, sot.rPSFMag, sot.rPSFMagErr, sot.rApMag, sot.rApMagErr, sot.rKronMag, sot.rKronMagErr, sot.rinfoFlag, sot.rinfoFlag2, sot.rinfoFlag3, sot.rnFrames,
 sot.iippDetectID, sot.istackDetectID, sot.istackImageId, sot.ira, sot.idec, sot.iraErr, sot.idecErr, sot.iEpoch, sot.iPSFMag, sot.iPSFMagErr, sot.iApMag, sot.iApMagErr, sot.iKronMag, sot.iKronMagErr, sot.iinfoFlag, sot.iinfoFlag2, sot.iinfoFlag3, sot.inFrames,
 sot.zippDetectID, sot.zstackDetectID, sot.zstackImageId, sot.zra, sot.zdec, sot.zraErr, sot.zdecErr, sot.zEpoch, sot.zPSFMag, sot.zPSFMagErr, sot.zApMag, sot.zApMagErr, sot.zKronMag, sot.zKronMagErr, sot.zinfoFlag, sot.zinfoFlag2, sot.zinfoFlag3, sot.znFrames,
 sot.yippDetectID, sot.ystackDetectID, sot.ystackImageId, sot.yra, sot.ydec, sot.yraErr, sot.ydecErr, sot.yEpoch, sot.yPSFMag, sot.yPSFMagErr, sot.yApMag, sot.yApMagErr, sot.yKronMag, sot.yKronMagErr, sot.yinfoFlag, sot.yinfoFlag2, sot.yinfoFlag3, sot.ynFrames
 

 from fGetNearbyObjEq("""+",".join([str(ang0),str(ang1),str(radius/60.)])+""") nb
 inner join StackObjectThin sot on sot.objid=nb.objid

 where sot.primaryDetection = 1 
""" 
    return query
        
        

def query_function(params, constraints):
    import exception as exc
    params['ang'],params['r'] = parameters(params["NSIDE"],params['pixel'])    
    query   =  query_string(params['ang'][0],params['ang'][1],params['r'])
    jobs    = mastcasjobs.MastCasJobs(context="PanSTARRS_DR2")
    
    try:
        table = jobs.quick(query, task_name="python cone search")
    except Exception:
        print("Exception. code!=200")
        table =  exc.handling_exception(params,constraints)
        print("Extracted {} objects from PS1".format(len(table)))
        return table, jobs  

    table = fixcolnames(ascii.read(table))
    table = query_constraints(table, constraints)
    return table, jobs

def query_constraints(table,constraints):
    band_KronMag = table[''.join([constraints["band"],'KronMag'])]
    band_PSFMag  = table[''.join([constraints["band"],'PSFMag'])]

    if constraints['use']:
        if constraints["type"]=="galaxy":
            constraint = (band_KronMag - band_PSFMag) + 0.192 - 0.120*(band_KronMag - 21.) - 0.018*(band_KronMag - 21.)*(band_KronMag - 21.)
            list1 = np.where((table['gdec']>-999)*(table['gra']>-999)*(band_KronMag>-999)*(band_PSFMag>-999)*(constraint>0))  
        
        elif constraints["type"]=="star":
            constraint = (band_KronMag - band_PSFMag) + 0.192 - 0.120*(band_KronMag - 21.) - 0.018*(band_KronMag - 21.)*(band_KronMag - 21.)
            list1 = np.where((table['gdec']>-999)*(table['gra']>-999)*(band_KronMag>-999)*(band_PSFMag>-999)*(constraint<0))
        
        else:    
            list1 = np.where((table['gdec']>-999)*(table['gra']>-999)*(band_KronMag>-999)*(band_PSFMag>-999))
    else:
        list1 = np.where((table['gdec']>-999)*(table['gra']>-999))
    
    return table[list1]
